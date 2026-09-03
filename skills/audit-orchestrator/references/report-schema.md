# Audit Report Schema

The final report must contain:

```json
{
  "site": "https://example.com",
  "audited_at": "2026-09-03T10:30:00Z",
  "summary": {
    "total_findings": 2,
    "critical": 0,
    "high": 1,
    "medium": 1,
    "low": 0
  },
  "findings": []
}
```

## Finding schema

Every finding must contain:

```json
{
  "id": "F-001",
  "title": "Short description of the problem",
  "severity": "high",
  "evidence": "Concrete evidence supporting the finding.",
  "suggested_action": {
    "summary": "What should be changed and how.",
    "priority": "high"
  }
}
```

## Recommended additional fields

```json
{
  "category": "discoverability",
  "source_skill": "crawl-render-audit",
  "confidence": "high",
  "affected_urls": [],
  "mechanism": "Explanation of why the issue affects AI discoverability or engagement.",
  "evidence_details": []
}
```

Allowed categories: `discoverability`, `engagement`, `both`.

Allowed severities: `critical`, `high`, `medium`, `low`.

Evidence must describe an observable property. Prefer `0/12 product pages contain Product JSON-LD` over `The site has poor SEO.`

Suggested actions must be specific, technically plausible, prioritized, and connected to the detected mechanism.
