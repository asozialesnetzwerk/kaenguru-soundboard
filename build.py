import json
import re

output = open("build/index.md", "w+")

with open('info.json', 'r') as myfile:
    info = json.loads(myfile.read())

persons = info["personen"]
output.write("# Känguru-Soundboard:\n")
for book in info["bücher"]:
    output.write("## " + book["name"] + "\n")
    for chapter in book["kapitel"]:
        output.write("### " + chapter["name"] + "\n")
        for file_text in chapter["dateien"]:
            file = re.sub(r"[^a-zäöüß_-]+", "", file_text.lower().replace(" ", "_"))
            output.write("- " + persons[file_text.split("-")[0]]
                         + ": »[" + file_text.split("-")[1]
                         + "](files/" + file + ".mp3)«\n\n")
            output.write("<audio controls><source src='files/" + file + ".mp3' type='audio/mpeg'></audio>\n\n")
