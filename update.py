import requests
from datetime import datetime

BASE = "https://wkze.com/wp-content/uploads/2026/06/"

items = []

# Known structure: weekly show, 2 parts per episode
# We'll scan likely episode days + both hour slots

for day in range(1, 31):  # June days
    for hour in [19, 20]:  # 7pm / 8pm
        for minute in ["00"]:
            for second in ["03"]:
                filename = f"TR202606{15+day:02d}-{hour}{minute}{second}.mp3"
                url = BASE + filename

                r = requests.head(url)
                if r.status_code == 200:
                    dt = datetime.strptime(filename[2:16] + filename[17:23], "%Y%m%d%H%M%S")
                    pubdate = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

                    items.append(f"""
    <item>
      <title>{filename}</title>
      <enclosure url="{url}" type="audio/mpeg" />
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
