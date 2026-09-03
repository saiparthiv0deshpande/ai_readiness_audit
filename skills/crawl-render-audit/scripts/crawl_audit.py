#!/usr/bin/env python3

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import deque
from html.parser import HTMLParser

USER_AGENT = "BrandAIReadinessAudit/1.0"
MAX_PAGES = 20
TIMEOUT = 10

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.headings, self.text, self.links, self.jsonld = [], [], [], [], []
        self.images_without_alt = 0
        self._in_title = self._heading = self._in_jsonld = False
        self._jsonld_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title": self._in_title = True
        if tag in {"h1", "h2", "h3"}: self._heading = True
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "img" and not attrs.get("alt"): self.images_without_alt += 1
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._in_jsonld, self._jsonld_buffer = True, []

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
        if tag in {"h1", "h2", "h3"}: self._heading = False
        if tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._jsonld_buffer))
            self._jsonld_buffer, self._in_jsonld = [], False

    def handle_data(self, data):
        value = " ".join(data.split())
        if not value: return
        if self._in_title: self.title.append(value)
        if self._heading: self.headings.append(value)
        if self._in_jsonld: self._jsonld_buffer.append(data)
        self.text.append(value)

def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return {"ok": True, "status": response.status, "url": response.geturl(),
                    "content_type": response.headers.get("Content-Type", ""),
                    "body": response.read(2_000_000)}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "status": None, "url": url, "error": str(exc)}

def normalize_url(base, href):
    try:
        url = urllib.parse.urljoin(base, href)
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in {"http", "https"}: return None
        return urllib.parse.urlunparse(parsed._replace(fragment=""))
    except Exception:
        return None

def same_host(a, b):
    return urllib.parse.urlparse(a).netloc.lower() == urllib.parse.urlparse(b).netloc.lower()

def get_robots(base_url):
    parsed = urllib.parse.urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = urllib.robotparser.RobotFileParser(robots_url)
    try:
        parser.read()
        return parser
    except Exception:
        return None

def parse_jsonld(raw):
    results = []
    for block in raw:
        try:
            data = json.loads(block)
            if isinstance(data, dict): results.append(data)
            elif isinstance(data, list): results.extend(x for x in data if isinstance(x, dict))
        except Exception:
            results.append({"_invalid_json": True})
    return results

def crawl(start_url):
    start_url = start_url.rstrip("/")
    queue, visited, pages = deque([(start_url, 0)]), set(), []
    robots = get_robots(start_url)
    while queue and len(pages) < MAX_PAGES:
        url, depth = queue.popleft()
        if url in visited: continue
        visited.add(url)
        if robots is not None and not robots.can_fetch(USER_AGENT, url):
            pages.append({"url": url, "crawl_allowed": False})
            continue
        result = fetch(url)
        page = {"url": url, "depth": depth, "ok": result["ok"],
                "status": result.get("status"), "content_type": result.get("content_type")}
        if not result["ok"]:
            page["error"] = result.get("error")
            pages.append(page); continue
        if "text/html" not in result.get("content_type", ""):
            pages.append(page); continue
        parser = PageParser()
        html = result["body"].decode("utf-8", errors="replace")
        try: parser.feed(html)
        except Exception as exc: page["parse_error"] = str(exc)
        data = parse_jsonld(parser.jsonld)
        page.update({"final_url": result["url"], "title": " ".join(parser.title),
                     "headings": parser.headings[:20], "text_length": len(" ".join(parser.text)),
                     "links_found": len(parser.links), "images_without_alt": parser.images_without_alt,
                     "jsonld_count": len(data), "jsonld": data[:20],
                     "script_count": html.lower().count("<script"), "server_html_length": len(html)})
        pages.append(page)
        for href in parser.links:
            child = normalize_url(result["url"], href)
            if child and same_host(start_url, child) and child not in visited and len(queue) < MAX_PAGES * 2:
                queue.append((child, depth + 1))
    return {"site": start_url, "pages_crawled": len(pages), "robots_checked": robots is not None, "pages": pages}

def main():
    if len(sys.argv) != 2:
        print("Usage: crawl_audit.py <url>", file=sys.stderr); sys.exit(2)
    url = sys.argv[1]
    if not url.startswith(("http://", "https://")): url = "https://" + url
    print(json.dumps(crawl(url), indent=2))

if __name__ == "__main__": main()
