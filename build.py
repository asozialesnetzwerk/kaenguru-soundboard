import json
import re
import os

os.makedirs("build", exist_ok=True)
output = open("build/index.md", "w+")

with open('info.json', 'r') as myfile:
    info = json.loads(myfile.read())

def linkify(val):
    return "[🔗](#-" + re.sub(r"[^a-zäöüß0-9-]", "", val.lower().replace(" ", "-")) + ") "


persons_stuff = {}
persons = info["personen"]
output.write("# Känguru-Soundboard:\n")
for book in info["bücher"]:
    output.write("## " + linkify(book["name"]) + book["name"] + "\n")
    for chapter in book["kapitel"]:
        output.write("### " + linkify(chapter["name"]) + chapter["name"] + "\n")
        for file_text in chapter["dateien"]:
            file = re.sub(r"[^a-zäöüß0-9_-]+", "", file_text.lower().replace(" ", "_"))
            person = file_text.split("-")[0]
            to_write = "- " + persons[person] + ": »[" \
                       + file_text.split("-", 1)[1] \
                       + "](files/" + file + ".mp3)«\n\n" \
                       + "<audio controls><source src='files/" \
                       + file \
                       + ".mp3' type='audio/mpeg'></audio>\n\n"

            persons_stuff[person] = persons_stuff.get(person, "# " + persons[person] + "\n\n") + to_write
            output.write(to_write)


for key in persons_stuff:
    _dir = "build/" + key
    os.makedirs(_dir, exist_ok=True)
    open(_dir + "/index.md", "w+").write(persons_stuff[key].replace("(files/", "(../files/"))

