---
name: adr
description: Lay out the options for an architecture decision, or record a decision the owner has made as a one-page ADR in docs/adr/. Use when a technical choice comes up (library, structure, data model, provider, trade-off), or when the owner says "write an ADR" or "/adr".
---

# Architecture Decision Record

The owner decides. Claude lays out options and drafts the record.

## Steps

1. Read `docs/adr/README.md`: the next number, what is accepted and what is pending.
2. **If the owner has not decided yet:** present two or three real options. For each one give one line on how it works, what it costs and what it gives up. Recommend one and say why in two sentences. Stop and wait for the owner's decision.
3. **Once the owner decides:** copy `docs/adr/0000-template.md` to `docs/adr/NNNN-kebab-title.md` and fill it in.
   - One page at most.
   - The Trade-off section is mandatory: what we give up, and what would make us revisit the decision.
   - Write the decision the owner made, in the owner's terms. Do not add parts the owner did not decide.
4. Update the index in `docs/adr/README.md`: add the ADR to Accepted and remove it from Pending.
5. To change an accepted decision, write a new ADR and set the old one's status to `Superseded by NNNN`. Never rewrite the decision of an accepted ADR.

ADRs are written in English.
