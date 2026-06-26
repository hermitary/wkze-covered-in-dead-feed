import re
import requests
from datetime import datetime

BASE = "https://wkze.com/wp-content/uploads/2026/06/"

# We try a reasonable range of possible episode times (7–9 PM blocks)
candidates = []

for day in range(1, 30):  # June range (adjustable later if needed)
    for hour in [19, 20]:  # 7 PM and 8 PM shows
        for minute in ["00", "30"]:
            for second in ["03"]:
                filename = f"TR202606{15+day:02d}-{hour}{minute}{second}.mp3"
                url = BASE + filename

                r = requests.head(url)
                if r.status_code == 200:
                    candidates.append(url)

items = []

for link in sorted(candidates):
    filename = link.split("/")[-1]

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
    <link>https://wkze.com/covered-in-dead-archive/</link>
    <description>Auto-generated WKZE podcast feed</description>
    {''.join(items)}
  </channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
