import requests
import re
from datetime import datetime

ARCHIVE_URL = "https://wkze.com/covered-in-dead-archive/"

html = requests.get(ARCHIVE_URL).text

# Pull every MP3 link directly from raw page text
mp3_links = sorted(set(re.findall(r"https://wkze\.com/wp-content/uploads/\d{4}/\d{2}/TR\d{8}-\d{6}\.mp3", html)))

items = []

for link in mp3_links:
    filename = link.split("/")[-1]

    # Try to extract date/time from filename
    match = re.search(r"TR(\d{8})-(\d{6})", filename)
    if match:
        dt = datetime.strptime(match.group(1) + match.group(2), "%Y%m%d%H%M%S")
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
    <description>Auto-generated WKZE Covered in Dead feed</description>
    {''.join(items)}
  </channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
