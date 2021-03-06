import json

output = open("index.md", "w+")

with open('info.json', 'r') as myfile:
    info = json.loads(myfile.read())

persons = info["personen"]
output.write("# Känguru-Soundboard:\n")
for book in info["bücher"]:
    output.write("## " + book["name"] + "\n")
    for chapter in book["kapitel"]:
        output.write("### " + chapter["name"] + "\n")
        for file in chapter["dateien"]:
            output.write("- " + persons[file.split("-")[0]] + ": \"[" + file.split("-")[1].replace("_", " ") + "](files/" + file + ".mp3)\"\n\n")
            output.write("<audio controls><source src='files/" + file + " type='audio/mpeg'></audio>\n")