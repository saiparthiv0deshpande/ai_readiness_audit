#!/usr/bin/env python3

import json
import re
import sys
import urllib.request
from html.parser import HTMLParser

USER_AGENT = "BrandAIReadinessAudit/1.0"
TIMEOUT = 10

class EngagementParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.headings, self.links, self.text = [], [], [], []
        self.in_title = self.in_heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title": self.in_title = True
        if tag in {"h1", "h2", "h3"}: self.in_heading = True
        if tag == "a" and attrs.get("href"):
            self.links.append({"href": attrs["href"], "text": ""})

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag in {"h1", "h2", "h3"}: self.in_heading = False

    def handle_data(self, data):
        value = " ".join(data.split())
        if not value: return
        if self.in_title: self.title.append(value)
        if self.in_heading: self.headings.append(value)
        self.text.append(value)
        if self.links:
            self.links[-1]["text"] = (self.links[-1]["text"] + " " + value).strip()

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.geturl(), response.read(2_000_000).decode("utf-8", errors="replace")

def count_terms(text, terms):
    lowered = text.lower()
    return {term: len(re.findall(r"\b" + re.escape(term) + r"\b", lowered)) for term in terms}

def main():
    if len(sys.argv) != 2:
        print("Usage: engagement_audit.py <url>", file=sys.stderr); sys.exit(2)
    url = sys.argv[1]
    if not url.startswith(("http://", "https://")): url = "https://" + url
    try: final_url, html = fetch(url)
    except Exception as exc:
        print(json.dumps({"skill":"engagement-audit","url":url,"error":str(exc)}, indent=2)); return
    parser = EngagementParser(); parser.feed(html)
    text = " ".join(parser.text)
    result = {
        "skill":"engagement-audit", "url":url, "final_url":final_url,
        "title":" ".join(parser.title), "headings":parser.headings[:20],
        "text_length":len(text),
        "internal_links":len([x for x in parser.links if x["href"].startswith(("/", "#"))]),
        "navigation_signals":count_terms(text,["products","services","solutions","pricing","about","contact","shop","features","resources"]),
        "action_signals":count_terms(text,["buy","book","contact","demo","get started","learn more","request","quote","sign up"]),
        "content_signals":count_terms(text,["price","pricing","features","specifications","services","product"]),
        "sample_links":parser.links[:50]
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
