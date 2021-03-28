#!/usr/bin/env python3
import json
import re
import os
import shutil

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

os.makedirs("build", exist_ok=True)
index_md = open("build/index.md", "w+")

with open('info.json', 'r') as my_file:
    info = json.loads(my_file.read())


def linkify(val):
    return "[🔗](#-{0}) ".format(re.sub(r"[^a-zäöüß0-9-]", "", val.lower().replace(" ", "-")))


rss_items = ""

persons_stuff = {}
persons = info["personen"]
index_md.write("# Känguru-Soundboard:\n")
for book in info["bücher"]:
    book_name = book["name"]
    index_md.write("## " + linkify(book_name) + book_name + "\n")
    for chapter in book["kapitel"]:
        chapter_name = chapter["name"]
        index_md.write("### " + linkify(chapter_name) + chapter_name + "\n")
        for file_text in chapter["dateien"]:
            file = re.sub(r"[^a-zäöüß0-9_-]+", "", file_text.lower().replace(" ", "_"))
            person = file_text.split("-")[0]
            to_write = ": »[" \
                       + file_text.split("-", 1)[1] \
                       + "](files/" + file + ".mp3)«\n\n" \
                       + "<audio controls><source src='files/" \
                       + file \
                       + ".mp3' type='audio/mpeg'></audio>\n\n"

            persons_stuff[person] = persons_stuff.get(person, "# " + persons[person] + "\n\n") \
                                    + "- " + persons[person] + to_write
            index_md.write("- [" + persons[person] + "](" + person + ")" + to_write)
            # rss:
            title_file_name = persons[file_text.split("-", 1)[0]] + ": »" + file_text.split("-", 1)[1] + "«"
            rss_items += item_string.format(
                title=title_string.format(book=book_name, chapter=chapter_name.split(":")[0],
                                          file_name=title_file_name), file_name=file) + "\n"

# pages for every person:
for key in persons_stuff:
    _dir = "build/" + key
    os.makedirs(_dir, exist_ok=True)
    open(_dir + "/index.md", "w+").write(
        persons_stuff[key].replace("(files/", "(../files/").replace("src='files/", "src='../files/"))

# write rss:
with open("build/feed.rss", "w") as feed:
    feed.write(rss_string.format(items=rss_items))

# copy files to build folder:
shutil.copytree("files", "build/files", dirs_exist_ok=True)
shutil.copy2("_config.yml", "build/")
shutil.copy2("icon.svg", "build/")
