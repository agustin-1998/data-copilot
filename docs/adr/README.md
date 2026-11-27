# Architecture Decision Records

One page per decision, each with its trade-off. New records start from [0000-template.md](0000-template.md).

## Accepted

- [0001. LLM strategy: two entry points over one core](0001-llm-strategy-two-entry-points.md)
- [0002. Repository layout: one Python package and a separate web app](0002-repository-layout.md)
- [0003. Sample dataset: Olist with synthetic personal data](0003-sample-dataset-olist.md)
- [0004. Database migrations: Alembic with hand-written SQL](0004-database-migrations-alembic.md)

## Pending

Roughly in the order we need them:

1. **Semantic layer format.** File format, where it lives, and how metrics and personal-data columns are described.
2. **SQL validation approach.** How we enforce SELECT only, the table allow-list and LIMIT.
3. **Hiding personal data from the model.** At which points personal columns are removed or masked.
4. **Web app model provider.** Which free-tier model API the web app's LangGraph agent uses, and the fallback chain.
5. **"Expensive query" for human approval.** What we measure and the threshold.
6. **Cache for repeated questions.** Cache key, storage and invalidation.
7. **Eval scoring.** How two result sets are compared (row order, rounding, column names).
8. **Deployment.** Where the online demo runs. AWS is part of the practice stack.
