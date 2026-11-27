# 0003. Sample dataset: Olist with synthetic personal data

- **Status:** Accepted
- **Date:** 2026-11-27

> I chose the Olist dataset (about 100k real orders from 2016 to 2018) with fake names, emails and phones added by the seed, because it is real and messy enough to make the semantic layer matter, big enough to practice indexes, and the fake personal data lets me prove the model never sees it; what I pay is that the personal data is invented, the dates are old and the license is non-commercial; if the project needs commercial use or newer data, I move to a generated dataset.

## Context

The agent needs an e-commerce database with dates and regions ("sales in October by region"), columns with personal data to hide from the model, enough volume for indexes and "expensive" queries, and messy statuses (canceled, unavailable) so that "what counts as a sale" is a real question. Anyone who clones the repository must get the exact same data with one command, because the eval answers depend on it.

## Options considered

1. **Olist plus synthetic personal data.** Real Brazilian marketplace data from Kaggle, anonymized, so personal columns are added with Faker.
2. **AdventureWorks for PostgreSQL.** Microsoft's sample with personal data and sales territories, but about 68 tables in 5 schemas: the semantic layer would eat week 1.
3. **Our own generator with Faker.** Full control and planted edge cases, but half a day of work and data that is less convincing in a demo.

Northwind was discarded: 830 orders are too few for indexes or expensive queries.

## Decision

Option 1:

- **Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
- **Distribution:** an unmodified copy of the Kaggle zip in this repository's GitHub Release `data-olist-v1`. The seed downloads it and stops unless its SHA-256 is `967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784`.
- **What the seed loads and changes:**
  - Every file except geolocation (1M rows; the region comes from the state).
  - Product categories in English, from the dataset's own translation table. Two categories missing from that table are translated by hand.
  - No review comment title or message: free text in Portuguese that may contain personal data.
  - Customers get a fake name, email (example domains only) and phone from Faker (`pt_BR`, fixed seed). One identity per real person (`customer_unique_id`), because Olist creates a new `customer_id` for every order.
  - A `regions` table maps the 27 states to Brazil's 5 regions.
- **Idempotent seed:** one transaction empties the tables and loads them again, so running it twice gives the same database, and a failed run leaves the old data intact.

## Trade-off

- The personal data is invented. It shows that the model never sees personal columns, but not how real personal data behaves.
- The data covers 2016 to 2018: "last October" questions need a fixed reference date.
- Non-commercial license: fine for a portfolio, not for a product.
- Revisit if the project needs commercial use, newer data, or edge cases Olist does not have.

## Consequences

- Eval answers are computed on this exact data. Changing the dataset means a new release tag, a new checksum and recomputed answers.
- The README credits Olist and states the license.
- Grants for the reader and hiding personal data are decided in a separate ADR.
