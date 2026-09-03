# Freshness and Corroboration Checks

## Explicit dates

Inspect `<time datetime>`, datePublished, dateModified, article dates, product update dates, and visible updated timestamps.

## Missing freshness signals

Do not automatically report missing `dateModified` as a defect. Ask whether the fact can change, whether freshness matters, and whether another reliable freshness signal exists.

## Internal contradictions

Compare repeated facts across pages. Direct contradictions such as different founding years on pages describing the same organization are strong evidence.

## Product/service consistency

Compare names, prices, availability, specifications, and descriptions for the same entity/version. Flag direct contradictions only when pages appear to describe the same entity/version.

## Entity identity

Look for consistent organization name, official domain, Organization schema, logo, contact information, address, social profiles, sameAs references, and consistent descriptions.

## External corroboration

When external search is available, select independent and relevant sources such as official registries, reputable publications, established directories, or authoritative industry sources. Do not treat one external source as definitive proof.

## Severity

- Critical: major contradictory identity information likely to cause serious entity confusion
- High: important current information is internally contradictory or materially stale
- Medium: freshness is unclear for dynamic information or identity signals are incomplete
- Low: useful but non-critical corroboration or metadata improvement
