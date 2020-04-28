import json
import re
import sys

file = open(sys.argv[1], "r")
Lines = file.readlines()
jsAry = []
content = [line.strip() for line in Lines]
for i in range(0, len(content)):
    x = re.search("^Write", content[i])
    if (x):
        y = content[i].split()
        index = y.index('at')
        js = {}
        js["Memory Address"] = y[index + 1]
        index = y.index('by')
        Thread = re.split(":", y[index + 2])
        js["Write_thread"] = y[index + 1] + ' ' + Thread[0]
        y = content[i + 1].split()
        for item in y:
            if (re.search("^/", item)):
                file = item.rsplit("/", 1)
                js["file loaction"] = file[0]
                location = file[1].split(":")
                js["write file name"] = location[0]
                js["write line #"] = location[1]
                js["write symbol position"] = location[2]
        jsAry.append(js)
    x = re.search("^Previous read", content[i])
    if (x):
        y = content[i].split()
        index = y.index('at')
        for item in jsAry:
            if (item["Memory Address"] == y[index + 1]):
                index = y.index('by')
                Thread = re.split(":", y[index + 2])
                item["Read_thread"] = y[index + 1] + ' ' + Thread[0]
                y = content[i + 1].split()
                for item1 in y:
                    if (re.search("^/", item1)):
                        file = item1.rsplit("/", 1)
                        location = file[1].split(":")
                        item["read file name"] = location[0]
                        item["read line #"] = location[1]
                        item["read symbol position"] = location[2]
                        item["tool"] = "archer"

    x = re.search("^Read", content[i])
    if (x):
        y = content[i].split()
        index = y.index('at')
        js = {}
        js["Memory Address"] = y[index + 1]
        index = y.index('by')
        Thread = re.split(":", y[index + 2])
        js["Write_thread"] = y[index + 1] + ' ' + Thread[0]
        y = content[i + 1].split()
        for item in y:
            if (re.search("^/", item)):
                file = item.rsplit("/", 1)
                js["file loaction"] = file[0]
                location = file[1].split(":")
                js["Read file name"] = location[0]
                js["Read line #"] = location[1]
                js["Read symbol position"] = location[2]
        jsAry.append(js)
    x = re.search("^Previous write", content[i])
    if (x):
        y = content[i].split()
        index = y.index('at')
        for item in jsAry:
            if (item["Memory Address"] == y[index + 1]):
                index = y.index('by')
                Thread = re.split(":", y[index + 2])
                item["Write_thread"] = y[index + 1] + ' ' + Thread[0]
                y = content[i + 1].split()
                for item1 in y:
                    if (re.search("^/", item1)):
                        file = item1.rsplit("/", 1)
                        location = file[1].split(":")
                        item["write file name"] = location[0]
                        item["write line #"] = location[1]
                        item["write symbol position"] = location[2]
                        item["tool"] = "archer"

js = {}
for i in range(len(jsAry)):
    js[i] = jsAry[i]

r = json.dumps(js)
print(r)