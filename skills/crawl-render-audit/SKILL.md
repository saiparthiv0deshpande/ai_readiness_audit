---
name: crawl-render-audit
description: Audit a website's machine accessibility, crawlability, readable content, JavaScript rendering, structured data, and internal links. Use when determining whether AI agents or crawlers can reach, read, and extract important information from a website.
license: MIT
---

# Crawl and Render Audit

## Purpose

Determine whether important website information can be reached by automated readers, read as machine-accessible content, and identified as explicit facts.

## Input

A public HTTP/HTTPS website URL.

## Procedure

1. Run `scripts/crawl_audit.py <URL>`.
2. Review the returned JSON.
3. Inspect the homepage and a representative set of important internal pages.
4. Where browser rendering is available, compare server-delivered HTML with rendered content.
5. Check structured data.
6. Identify important facts that appear visually present but are not represented in accessible text or structured data.
7. Report only evidence-backed issues.

## Checks

Evaluate HTTP accessibility, robots.txt, internal-link reachability, HTTP errors, title and heading presence, visible text extraction, structured data, JSON-LD syntax, relevant schema types, image alt text, JavaScript-dependent content, and content present only after rendering.

Detailed rules are in `references/checks.md`.

## Important distinction

Do not report "The page uses JavaScript" as a defect. Only report a rendering problem when important information appears dependent on client-side rendering and there is evidence that the information is not available in the server-delivered representation.

## Output

Return:

```json
{
  "skill": "crawl-render-audit",
  "findings": [],
  "observations": [],
  "limitations": []
}
```

## Safety

Read-only only. Do not submit forms, authenticate, modify content, upload files, crawl unlimited URLs, bypass robots.txt, or repeatedly request failed pages.
