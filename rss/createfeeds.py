import json
import re

rss_string = '''<?xml version="1.0" encoding="UTF-8"?>
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

item_string = '''    <item>
      <title>{title}</title>
      <enclosure url="https://asozial.org/kaenguru-soundboard/files/{file_name}.mp3"
                 type="audio/mpeg">
      <guid>{file_name}</guid>
    </item>'''

title_string = "[{book}, {chapter}] {file_name}"

with open("info.json") as file:
    files = json.loads(file.read())

persons = files["personen"]
items = ""
for book in files["bücher"]:
    book_name = book["name"]
    for chapter in book["kapitel"]:
        chapter_name = chapter["name"].split(":")[0]
        for file_text in chapter["dateien"]:
            file = re.sub(r"[^a-zäöüß_-]+", "", file_text.lower().replace(" ", "_"))
            title_file_name = persons[file_text.split("-")[0]] + ": »" + file_text.split("-")[1] + "«"
            items += item_string.format(title=title_string.format(book=book_name, chapter=chapter_name, file_name=title_file_name), file_name=file) + "\n"

with open("feed.rss", "w") as feed:
    feed.write(rss_string.format(items=items))



