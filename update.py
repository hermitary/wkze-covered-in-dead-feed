from playwright.sync_api import sync_playwright
import re

ARCHIVE_URL = "https://wkze.com/covered-in-dead-archive/"

mp3_links = set()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(ARCHIVE_URL)
    content = page.content()
    browser.close()

    mp3_links = set(re.findall(r"https://wkze\.com/wp-content/uploads/\d{4}/\d{2}/TR\d{8}-\d{6}\.mp3", content))

items = []

for link in sorted(mp3_links):
    filename = link.split("/")[-1]
    items.append(f"""
    <item>
      <title>{filename}</title>
      <enclosure url="{link}" type="audio/mpeg" />
      <guid>{filename}</guid>
    </item>
    """)

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Covered in Dead (WKZE Archive)</title>
    <link>{ARCHIVE_URL}</link>
    <description>Auto-generated WKZE podcast feed</description>
    {''.join(items)}
  </channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
