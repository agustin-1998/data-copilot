# Architecture Decision Records

One page per decision, each with its trade-off. New records start from [0000-template.md](0000-template.md).

## Accepted

- [0001. LLM strategy: two entry points over one core](0001-llm-strategy-two-entry-points.md)
- [0002. Repository layout: one Python package and a separate web app](0002-repository-layout.md)

## Pending

Roughly in the order we need them:

1. **Sample dataset.** Which e-commerce data, its size, and how it is loaded.
2. **Database migrations.** Which tool and where migrations live. Week 3 needs a real expand-and-contract migration.
3. **Semantic layer format.** File format, where it lives, and how metrics and personal-data columns are described.
4. **SQL validation approach.** How we enforce SELECT only, the table allow-list and LIMIT.
5. **Hiding personal data from the model.** At which points personal columns are removed or masked.
6. **Web app model provider.** Which free-tier model API the web app's LangGraph agent uses, and the fallback chain.
7. **"Expensive query" for human approval.** What we measure and the threshold.
8. **Cache for repeated questions.** Cache key, storage and invalidation.
9. **Eval scoring.** How two result sets are compared (row order, rounding, column names).
10. **Deployment.** Where the online demo runs. AWS is part of the practice stack.
