import json

rssstring = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Kaenguru Soundboard</title>
    <description>Ein Soundboard zu den Känguru Chroniken</description>
    <language>de-de</language>
    <link>https://asozial.org/kaenguru-soundboard</link>
    {items}
  </channel>
</rss>
'''
itemstring = '''    <item>
      <title>{title}</title>
      <enclosure url="https://asozial.org/kaenguru-soundboard/files/{filename}"
                 type="audio/mpeg">
      <guid>{filename}</guid>
    </item>'''
titlestring = "[{book}, {chapter}] {filename}"

with open("info.json") as file:
    files = json.loads(file.read())

items = ""
for book in files["bücher"]:
    bookname = book["name"]
    for chapter in book["kapitel"]:
        chaptername = chapter["name"]
        for file in chapter["dateien"]:
            items += itemstring.format(title=titlestring.format(book=bookname, chapter=chaptername, filename=file), filename=file) + "\n"

with open("feed.rss", "w") as feed:
    feed.write(rssstring.format(items=items))



