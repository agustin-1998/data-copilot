# Data Copilot

[![backend](https://github.com/agustin-1998/data-copilot/actions/workflows/backend.yml/badge.svg)](https://github.com/agustin-1998/data-copilot/actions/workflows/backend.yml)

A text-to-SQL agent: ask a question about an e-commerce business in plain language and get back the number, the SQL it ran and a chart.

Work in progress. Design decisions are recorded in [docs/adr](docs/adr/README.md).

## Data

The sample data is the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Credit goes to Olist.

The seed downloads an unmodified copy from this repository's [`data-olist-v1` release](https://github.com/agustin-1998/data-copilot/releases/tag/data-olist-v1), checks its checksum and then changes it while loading: product categories in English, review comments left out, and synthetic names, emails and phones for customers. See [ADR 0003](docs/adr/0003-sample-dataset-olist.md).
