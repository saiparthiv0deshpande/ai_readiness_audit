#!/usr/bin/env python3

import json
import re
import sys
import urllib.request
from html.parser import HTMLParser

USER_AGENT = "BrandAIReadinessAudit/1.0"
TIMEOUT = 10

class FactParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.headings, self.text, self.times, self.meta, self.jsonld = [], [], [], [], {}, []
        self.in_title = self.in_heading = self.in_jsonld = False
        self.jsonld_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title": self.in_title = True
        if tag in {"h1", "h2", "h3"}: self.in_heading = True
        if tag == "time" and attrs.get("datetime"): self.times.append(attrs["datetime"])
        if tag == "meta":
            name = attrs.get("name") or attrs.get("property")
            if name and attrs.get("content"): self.meta[name.lower()] = attrs["content"]
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.in_jsonld, self.jsonld_buffer = True, []

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag in {"h1", "h2", "h3"}: self.in_heading = False
        if tag == "script" and self.in_jsonld:
            self.jsonld.append("".join(self.jsonld_buffer)); self.in_jsonld = False; self.jsonld_buffer = []

    def handle_data(self, data):
        value = " ".join(data.split())
        if not value: return
        if self.in_title: self.title.append(value)
        if self.in_heading: self.headings.append(value)
        if self.in_jsonld: self.jsonld_buffer.append(data)
        self.text.append(value)

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read(2_000_000).decode("utf-8", errors="replace")

def parse_jsonld(blocks):
    result = []
    for block in blocks:
        try:
            value = json.loads(block)
            if isinstance(value, list): result.extend(x for x in value if isinstance(x, dict))
            elif isinstance(value, dict): result.append(value)
        except Exception: pass
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: fact_audit.py <url>", file=sys.stderr); sys.exit(2)
    url = sys.argv[1]
    if not url.startswith(("http://", "https://")): url = "https://" + url
    try: html = fetch(url)
    except Exception as exc:
        print(json.dumps({"skill":"freshness-corroboration","url":url,"error":str(exc)}, indent=2)); return
    parser = FactParser(); parser.feed(html)
    text = " ".join(parser.text)
    dates = list(parser.times)
    for key in {"article:published_time","article:modified_time","date","last-modified","og:updated_time"}:
        if key in parser.meta: dates.append(parser.meta[key])
    for item in parse_jsonld(parser.jsonld):
        for key in ("datePublished", "dateModified"):
            if item.get(key): dates.append(str(item[key]))
    result = {
        "skill":"freshness-corroboration", "url":url, "title":" ".join(parser.title),
        "headings":parser.headings[:20], "text_length":len(text),
        "freshness_signals":dates[:30], "metadata":parser.meta,
        "jsonld":parse_jsonld(parser.jsonld)[:20],
        "contact_signals":{
            "email_count":len(re.findall(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", text, re.I)),
            "phone_count":len(re.findall(r"(?:\+?\d[\d\s().-]{7,}\d)", text))
        }
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
