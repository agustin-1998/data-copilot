---
name: teach
description: Teach the owner a topic before it is used in the project (for example LangGraph state, PostgreSQL indexes, Pydantic models, GitHub Actions). Use when the owner says "teach me X", "explain X before we use it", "/teach", or when a new concept is about to enter the code and the owner has not learned it yet.
---

# Teach a topic

Goal: the owner can explain the topic in a job interview, in their own words, and knows where it shows up in this project.

Speak Spanish (Rioplatense). Keep code and technical terms in English.

## Steps

1. **Scope.** One topic at a time. If the topic is broad, split it, teach the first piece and list the rest for later.
2. **Simple version.** Eight lines or fewer. Compare it with something the owner already knows (use the analogy map in `CLAUDE.local.md` when it exists). Say where the analogy breaks.
3. **Technical layer.** How it really works. The one or two details interviewers usually ask about. A small example in this project's domain (orders, customers, sales), not `foo`/`bar`.
4. **Where it lands.** Which part of Data Copilot uses it, and why we need it there.
5. **Explain it back, twice.** Ask the owner to explain it in their own words. Then ask for a second explanation applied to a different case, framed as an interview follow-up question.
6. **Correct.** Only what is wrong or important. Skip style and wording nitpicks.
7. **Close.** One-line summary and one likely interview question the owner can practice.

## Do not

- Do not write the owner's core code as part of a lesson. Examples stay small and illustrative.
- Do not move to the next topic until the owner has explained this one.
- Do not quiz the owner on things they already know well (for example what a LangSmith trace stores).
