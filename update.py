import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

ARCHIVE_URL = "https://wkze.com/covered-in-dead-archive/"

r = requests.get(ARCHIVE_URL)
soup = BeautifulSoup(r.text, "html.parser")

mp3_links = set()

for a in soup.find_all("a", href=True):
    if ".mp3" in a["href"]:
        mp3_links.add(a["href"])

items = []

for link in sorted(mp3_links):
    filename = link.split("/")[-1]

    match = re.search(r"TR(\d{8})-(\d{6})", filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        dt = datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
        pubdate = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    else:
        pubdate = ""

    items.append(f"""
    <item>
      <title>{filename}</title>
      <enclosure url="{link}" type="audio/mpeg" />
      <guid>{filename}</guid>
      <pubDate>{pubdate}</pubDate>
    </item>
    """)

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Covered in Dead (WKZE Archive)</title>
    <link>{ARCHIVE_URL}</link>
    <description>Auto-generated WKZE archive feed</description>
    {''.join(items)}
  </channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
