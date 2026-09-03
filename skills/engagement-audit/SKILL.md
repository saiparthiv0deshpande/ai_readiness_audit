---
name: engagement-audit
description: Audit the on-site experience for visitors arriving from AI assistants, including orientation, context continuity, relevant information visibility, navigation, calls to action, and conversion paths. Use when determining why visitors who arrive at a website may fail to understand the context, find the information promised by an AI answer, or continue their journey.
license: MIT
---

# On-Site Engagement Audit

## Purpose

Evaluate whether a visitor arriving from an AI recommendation can quickly understand the website, locate relevant information, and continue toward a useful next action.

This is not a generic visual-design audit. Focus on information continuity between `AI recommendation -> website -> user action`.

## Procedure

1. Run `scripts/engagement_audit.py <URL>`.
2. Inspect the homepage.
3. Inspect representative high-value pages such as product, service, pricing, contact, and category pages.
4. Determine what the website is, what the brand offers, whether the value proposition is clear, whether important information is easy to find, whether relevant information is internally linked, whether users have clear next actions, and whether a likely AI referral can be followed naturally.
5. Avoid subjective aesthetic judgments.
6. Report only observable problems.

## Context-retention principle

A strong landing experience should allow a visitor to answer quickly:

1. Where am I?
2. What is this brand/product/service?
3. Why am I seeing this page?
4. Where is the information I came for?
5. What should I do next?

## Output

```json
{
  "skill": "engagement-audit",
  "findings": [],
  "observations": [],
  "limitations": []
}
```

Without an actual AI referral query, do not claim that the website fails to preserve a specific conversation context. Report structural weaknesses that would make context continuity difficult.
