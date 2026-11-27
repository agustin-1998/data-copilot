# Architecture Decision Records

One page per decision, each with its trade-off. New records start from [0000-template.md](0000-template.md).

## Accepted

- [0001. LLM strategy: two entry points over one core](0001-llm-strategy-two-entry-points.md)

## Pending

To decide in week 1, roughly in this order:

1. **Web app model provider.** Which free-tier model API the web app's LangGraph agent uses, and the fallback chain.
2. **Repository layout.** Where the API, the web app and shared files live, and which tooling each part uses.
3. **Sample dataset.** Which e-commerce data, its size, and how it is loaded.
4. **Semantic layer format.** File format, where it lives, and how metrics and personal-data columns are described.
5. **SQL validation approach.** How we enforce SELECT only, the table allow-list and LIMIT.
6. **Hiding personal data from the model.** At which points personal columns are removed or masked.
7. **"Expensive query" for human approval.** What we measure and the threshold.
8. **Cache for repeated questions.** Cache key, storage and invalidation.
9. **Eval scoring.** How two result sets are compared (row order, rounding, column names).
