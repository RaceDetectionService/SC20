import json
import re
import sys

file = open(sys.argv[1], "r")
Lines = file.readlines()
jsAry = []
content = [line.strip() for line in Lines]
for i in range(0, len(content)):
    x = re.search("Write", content[i])
    if (x):
        y = content[i].split()
        js = {}
        if (re.search("^/", y[0])):
            file = y[0].rsplit("/", 1)
            location = file[1].split(":")
            f = location[0].split("(")
            js["write file name"] = f[0]
            line = f[1].split(")")
            js["write line #"] = line[0]
        x = re.search("Read", content[i + 1])
        if (x):
            y = content[i + 1].split()
            if (re.search("^/", y[0])):
                file = y[0].rsplit("/", 1)
                location = file[1].split(":")
                f = location[0].split("(")
                js["read file name"] = f[0]
                line = f[1].split(")")
                js["read line #"] = line[0]
            js["tool"] = "intel-instpector"
            jsAry.append(js)
    x = re.search("Read", content[i])
    if (x):
        y = content[i].split()
        js = {}
        if (re.search("^/", y[0])):
            file = y[0].rsplit("/", 1)
            location = file[1].split(":")
            f = location[0].split("(")
            js["read file name"] = f[0]
            line = f[1].split(")")
            js["read line #"] = line[0]
        x = re.search("Write", content[i + 1])
        if (x):
            y = content[i + 1].split()
            if (re.search("^/", y[0])):
                file = y[0].rsplit("/", 1)
                location = file[1].split(":")
                f = location[0].split("(")
                js["write file name"] = f[0]
                line = f[1].split(")")
                js["write line #"] = line[0]
            js["tool"] = "intel-instpector"
            jsAry.append(js)

js = {}
for i in range(len(jsAry)):
    js[i] = jsAry[i]

r = json.dumps(js)
print(r)