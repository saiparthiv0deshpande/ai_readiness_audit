# Crawl and Render Checks

## 1. HTTP accessibility

Check the homepage and selected internal pages. Record final URL, HTTP status, redirects, content type, and response failures.

Create a finding when an important page consistently fails to return a successful HTML response. Do not flag temporary failures without sufficient evidence.

## 2. Robots.txt

Retrieve `/robots.txt` and determine whether crawling of important paths appears disallowed. Only report a potential discoverability problem when the relevant page or path is actually affected. Do not assume every robots.txt directive blocks every AI system.

## 3. Internal reachability

Build a bounded crawl from the homepage. Record discovered URLs, successful URLs, failed URLs, and depth. Important pages should be reachable through normal internal navigation.

Flag important content that appears orphaned or unreachable from the crawl entrypoint.

## 4. Machine-readable text

Extract readable text and look for important factual information such as product names, service descriptions, prices, availability, locations, policies, and contact information. Report when important information appears primarily in inaccessible non-textual structures and there is insufficient equivalent text.

## 5. Structured data

Inspect JSON-LD and other structured-data blocks. Check valid JSON, schema types, applicable required properties, and consistency with visible content. Relevant examples include Product, Offer, Organization, LocalBusiness, Article, and FAQPage.

Do not claim that absence of schema means AI cannot understand a site. Describe the concrete extraction limitation instead.

## 6. JavaScript rendering

Compare server HTML with browser-rendered content when a browser is available. Flag only when important content is absent from server HTML, appears after rendering, and is materially relevant to understanding the page.

## 7. Images and non-text content

Inspect important images for meaningful alternative text. Prioritize images that communicate product identity, specifications, diagrams, prices, policies, or essential service information.

## 8. Evidence quality

Prefer quantitative evidence such as `0/12 product pages contain Product JSON-LD`, `7/20 sampled pages return HTTP 404`, or `3 important pages are unreachable from the bounded crawl`.
