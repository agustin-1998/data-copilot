# 0001. LLM strategy: two entry points over one core

- **Status:** Accepted
- **Date:** 2026-11-27

> I chose one core with two entry points, a local MCP server that uses the connected agent's model and a web app whose LangGraph agent calls a free-tier API, because people can use the agent they already have without me paying for it and every safety rule lives in one place; what I pay is that locally the agent, not my graph, decides the order of the steps, and two entry points to maintain; if Claude Code or the other agents add MCP sampling, I move LangGraph inside the MCP server and use the agent's model.

## Context

Data Copilot needs a language model to turn questions into SQL. This is a portfolio project, so there is no budget for a paid model API. People who clone the repository should be able to use it with the agent they already have (Claude Code, Codex, Gemini CLI). There should also be an online demo that anyone can try without installing anything. The owner's personal subscription must never serve other people's requests.

MCP lets an agent call a server's tools. A server can only use the agent's model through MCP sampling, and Claude Code does not support sampling ([anthropics/claude-code#1785](https://github.com/anthropics/claude-code/issues/1785) is still open on 2026-11-27).

## Options considered

1. **One model API for everything.** LangGraph calls a model API in every case. Simple, but people who clone the repository cannot use their own agent, and all usage limits fall on the owner.
2. **Agent CLIs as the model backend.** The server runs `claude -p`, `codex exec` or similar for each question. This ties the online demo to the owner's subscription, which Anthropic's terms do not allow for third-party products, adds seconds of start-up to every call, and gives a model with shell access to text read from the database.
3. **LangGraph inside the MCP server, using the agent's model through sampling.** The cleanest fit, but Claude Code does not support sampling.
4. **Two entry points over one core.** Chosen.

## Decision

One core (semantic layer, SQL validation, read-only execution) with two entry points:

- **Local, through MCP.** Whoever clones the repository connects their own agent to the Data Copilot MCP server. The agent's model writes the SQL. The server's tools give it the semantic layer, validate the SQL and execute it. Each person uses their own plan.
- **Online, through the web app.** Next.js, then FastAPI, then LangGraph, which calls a model API on a free tier. The provider and the fallback chain are decided in a separate ADR.

## Trade-off

- Locally, the agent decides the order of the steps, not our LangGraph graph.
- Answer quality in the local entry point depends on each person's agent and model. Our evals measure only the online entry point.
- Two entry points to build, test and document.
- Free tiers have rate limits and can change or disappear. The online demo needs its own rate limiting and a fallback.
- Revisit if Claude Code or the other agents add MCP sampling: LangGraph could then run inside the MCP server with the agent's model.

## Consequences

- Every safety rule (SELECT only, table allow-list, LIMIT, read-only role, personal data hidden from the model) lives in the core, never in an entry point.
- The tool that executes SQL always validates it itself and refuses SQL that fails. It never assumes the agent called the validation tool first.
- Personal data stays hidden in the local entry point too: tool results sent back to the agent never include personal columns, because the agent is also a model.
- The MCP server is no longer an extra. It is one of the two entry points.
- New pending decision: model provider and fallback chain for the web app.
