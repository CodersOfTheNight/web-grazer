# web-grazer
Yet another scraper

Why even consider?
------------------
It works just by providing correct config - no coding is required

Config example
--------------
```yaml
---
name: Python Org scrapper
description: Just scrape it for testing
site_root: https://www.python.org
start_page: /blogs
pages:
  - name: Blog
    link_pattern: /blog%
    mappings:
      - name: title
        path: h3[class="event-title"]/a
```
