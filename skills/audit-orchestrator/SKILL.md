---
name: audit-orchestrator
description: Audit a website for AI discoverability and on-site engagement by coordinating crawl, rendering, structured-data, freshness, corroboration, entity, and engagement checks. Use when a website must be evaluated for why AI assistants may fail to find, understand, trust, cite, or correctly represent it, or why visitors arriving from AI assistants may fail to engage.
license: MIT
---

# Brand AI Readiness Audit Orchestrator

## Purpose

You are the entrypoint for a read-only website audit.

Given a public website URL or domain, coordinate the specialist audit skills and produce one evidence-backed report.

The audit covers two dimensions:

1. Off-site AI discoverability
2. On-site engagement

Do not modify the target website. Do not submit forms. Do not authenticate. Do not perform destructive actions. Respect robots.txt and avoid excessive requests.

## Input

Accept a public HTTP/HTTPS URL or a domain that can be normalized to HTTPS.

## Procedure

### Step 1 — Normalize and validate the target

Normalize the input into a canonical HTTP/HTTPS URL. Reject local filesystem paths, localhost targets, private network targets, unsupported URL schemes, and authenticated URLs containing credentials.

### Step 2 — Run crawl/render audit

Use `crawl-render-audit`. Inspect crawl accessibility, robots.txt, important internal links, HTTP failures, machine-readable text, JavaScript-rendered content gaps where rendering is available, structured data, and important information hidden in non-textual elements.

### Step 3 — Run freshness/corroboration audit

Use `freshness-corroboration`. Inspect important factual claims, freshness signals, date metadata, inconsistent facts across important pages, entity identity signals, and external corroboration when an appropriate read-only web search capability is available.

Do not treat lack of external corroboration as proof that a claim is false.

### Step 4 — Run engagement audit

Use `engagement-audit`. Inspect homepage orientation, relevant landing pages, brand/entity identification, important product/service information, navigation, contextual continuity, calls to action, and contact/conversion paths.

### Step 5 — Validate evidence

Every finding must contain concrete evidence. Prefer URL, page count, HTTP status, extracted element, structured-data type, text excerpt, count or ratio, detected metadata, or navigation path.

If evidence is insufficient, downgrade the finding to a recommendation rather than reporting it as a definite defect.

### Step 6 — Deduplicate

Merge duplicate findings when they represent the same root cause and preserve the strongest evidence.

### Step 7 — Assign severity

Use:

- critical — severe issue likely to prevent important information from being discoverable or usable
- high — substantial issue affecting important information or user journeys
- medium — meaningful issue with limited scope or impact
- low — minor improvement opportunity

Do not assign high severity merely because a best practice is missing.

### Step 8 — Prioritize actions

Every suggested action should explain what should change, where it should change, why it addresses the detected mechanism, and what evidence supports the recommendation.

### Step 9 — Add proactive recommendations

Recommendations may identify useful improvements where no explicit defect was detected. Clearly distinguish recommendations from detected findings. Do not manufacture defects.

### Step 10 — Emit the final report

Return valid JSON following `references/report-schema.md`.

## Evidence rules

Never claim that an AI assistant definitely will or will not cite a website based only on one technical signal. Use mechanism-based language such as "may reduce extractability" or "creates a potential rendering gap".

A finding must be tied to observable evidence.

## Failure handling

If a specialist fails, record the limitation, continue with other specialists, and never fabricate results.

## Final quality check

Before returning the report verify that the site and audited_at exist, severity counts match findings, every finding has id/title/severity/evidence/suggested_action, findings are deduplicated, recommendations are actionable, and no live-site modification occurred.
