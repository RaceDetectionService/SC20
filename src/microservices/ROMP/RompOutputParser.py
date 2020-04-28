import json
import re
import sys

file = open(sys.argv[1], "r")
Lines = file.readlines()
jsAry = []
content = [line.strip() for line in Lines]
for i in range(0, len(content)):
    x = re.search("RAW", content[i])
    if (x):
        y = content[i].split()
        index = y.index('addr:')
        js = {}
        js["Memory Address"] = y[index + 1]
        y = content[i + 1].split()
        for i in range(len(y)):
            file = y[0].rsplit("/", 1)
            js["file loaction"] = file[0]
            location = file[1].split(":")
            filename = location[0].split('@')
            js["write file name"] = filename[0]
            js["write line #"] = location[1]
            js["write symbol position"] = y[1]
            file = y[3].rsplit("/", 1)
            js["file loaction"] = file[0]
            location = file[1].split(":")
            js["Read file name"] = filename[0]
            js["Read line #"] = location[1]
            js["Read symbol position"] = y[4]
            js["tool"] = "romp"
        jsAry.append(js)
js = {}
for i in range(len(jsAry)):
    js[i] = jsAry[i]

r = json.dumps(js)
print(r)
