---
name: freshness-corroboration
description: Audit important website facts for freshness, consistency, entity identity, and corroboration. Use when determining whether an AI assistant could encounter stale, conflicting, weakly supported, or ambiguous brand information.
license: MIT
---

# Freshness and Corroboration Audit

## Purpose

Determine whether important facts about a website's brand, products, or services are sufficiently current, consistent, and unambiguous for an automated system to interpret.

## Procedure

1. Run `scripts/fact_audit.py <URL>`.
2. Review extracted factual signals.
3. Identify important facts such as organization name, product/service names, prices, availability, locations, policies, dates, and contact details.
4. Check freshness indicators and compare repeated facts across important pages.
5. Look for identity ambiguity.
6. If a read-only external search capability is available, use it only for high-value claims where corroboration materially affects the assessment.
7. Distinguish detected inconsistency, stale signal, missing freshness signal, lack of corroboration, and actual contradiction.

## Important rule

Absence of a freshness signal is not proof that information is stale. Absence of external corroboration is not proof that a claim is false.

## Output

```json
{
  "skill": "freshness-corroboration",
  "findings": [],
  "observations": [],
  "limitations": []
}
```
