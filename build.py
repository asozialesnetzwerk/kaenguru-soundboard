#!/usr/bin/env python3
import json
import re
import os
import shutil

rss_string = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Kaenguru Soundboard{extra_title}</title>
    <description>Ein Soundboard zu den Känguru Chroniken{extra_desc}</description>
    <language>de-de</language>
    <link>https://asozial.org/kaenguru-soundboard/{extra_link}</link>
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

html_string = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="theme-color" content="#8B0000">
    <meta property="og:url" content="https://asozial.org/kaenguru-soundboard/{extra_link}" />
    <meta property="og:type" content="website" />
    <title>Känguru Soundboard{extra_title}</title>
    <meta property="og:title" content="Känguru Soundboard{extra_title}" />
    <meta property="og:description" content="Ein Soundboard zu den Känguru Chroniken{extra_desc}" />
    <style>
        :root {{
            --red: #8B0000;
            --white: #fefefe;
            --light-grey: #9e9e9e;
            --grey: #242424;
            --black: #000;
            --dark-grey: #111111;
            --light-red: #f00;
            --light-blue: #00bfff;
            --blue: #00f;
        }}
        * {{
            color: var(--white);
            background-color: var(--black);
        }}
        #container {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }}
        .a_hover {{
            text-decoration: none;
        }}
        .a_hover:hover {{
            text-decoration: underline;
        }}
        h1 {{
            color: var(--red);
        }}
    </style>
</head>
<body>
<div id="container">{content}</div>
<footer style="
position: fixed;
bottom: 20px;
left: 50%;
transform: translateX(-50%);
text-align: center;
color: var(--white);
background-color: transparent;
">
  Mit Liebe gebacken 🖤
  <a style="color: var(--red); background-color: transparent;"
     href="https://github.com/asozialesnetzwerk">
    Asoziales Netzwerk: Sektion GitHub
  </a>
</footer>
</body>
</html>
'''

os.makedirs("build", exist_ok=True)
# Känguru-Chroniken.\"\n---\n"

with open('info.json', 'r') as my_file:
    info = json.loads(my_file.read())


def name_to_id(val):
    return re.sub(r"[^a-zäöüß0-9-]", "", val.lower().replace(" ", "-"))


def create_anchor(href, inner_html, color="var(--red)", classes="a_hover"):
    return f"<a href='{href}' class='{classes}' style='color: {color};'>{inner_html}</a>"


def create_heading(heading_type, text):
    el_id = name_to_id(text)
    return f"<{heading_type} id='{el_id}'>" \
           f"{create_anchor('#' + el_id, '🔗 ' + text)}" \
           f"</{heading_type}>"


rss_items = ""

persons_stuff = {}
persons_rss = {}
persons = info["personen"]
index_html = "<h1>Känguru-Soundboard:</h1>"
for book in info["bücher"]:
    book_name = book["name"]
    index_html += create_heading("h2", book_name)
    for chapter in book["kapitel"]:
        chapter_name = chapter["name"]
        index_html += create_heading("h3", chapter_name) + "<ul>"
        for file_text in chapter["dateien"]:
            file = re.sub(r"[^a-zäöüß0-9_-]+", "", file_text.lower().replace(" ", "_"))
            full_file = f"files/{file}.mp3"
            person = file_text.split("-")[0]
            to_write = f": »{create_anchor(full_file, file_text.split('-', 1)[1], 'var(--light-grey)')}" \
                       f"«<br><audio controls><source src='{full_file}' type='audio/mpeg'></audio>"

            persons_stuff[person] = f"{persons_stuff.get(person, '')}<li>{persons[person]}" \
                                    f"{to_write}</li>"

            index_html += f"<li>{create_anchor(person, persons[person], 'var(--light-red)')}" \
                          f"{to_write}</li>"
            # rss:
            title_file_name = persons[file_text.split("-", 1)[0]] + ": »" + file_text.split("-", 1)[
                1] + "«"
            rss = item_string.format(
                title=title_string.format(book=book_name, chapter=chapter_name.split(":")[0],
                                          file_name=title_file_name), file_name=file) + "\n"
            rss_items += rss
            persons_rss[person] = persons_rss.get(person, "") + rss
        index_html += "</ul>"

# write main page:
open("build/index.html", "w+").write(html_string.format(extra_title="", extra_desc="",
                                                        extra_link="", content=index_html))

# pages for every person:
for key in persons_stuff:
    _dir = "build/" + key
    os.makedirs(_dir, exist_ok=True)
    person = persons[key].replace("Das", "dem").replace("Der", "dem").replace("Die", "der")
    content = "---\ntitle: \"Känguru-Soundboard\"\ndescription: \"Coole Sprüche/Sounds von " + person + " aus den Känguru-Chroniken.\"\n---\n" \
              + "# " + persons[key] + "\n\n" \
              + persons_stuff[key].replace("(files/", "(../files/").replace("src='files/",
                                                                            "src='../files/")
    extra_title = " (Coole Sprüche/Sounds von " + person + ")"
    extra_desc = " mit coolen Sprüchen/Sounds von " + person
    open(_dir + "/index.html", "w+").write(html_string.format(extra_title=extra_title,
                                                              extra_desc=extra_desc,
                                                              extra_link=key, content=content))
    # rss for every person:
    open(_dir + "/feed.rss", "w+") \
        .write(rss_string.format(items=persons_rss[key],
                                 extra_title=extra_title,
                                 extra_desc=extra_desc,
                                 extra_link=key))

# write rss:
with open("build/feed.rss", "w") as feed:
    feed.write(rss_string.format(items=rss_items, extra_title="", extra_desc="", extra_link=""))

# copy files to build folder:
shutil.copytree("files", "build/files", dirs_exist_ok=True)
shutil.copy2("icon.svg", "build/")
