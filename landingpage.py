from json import loads
from os import system as ossystem
from pieces import extendPieces
from py_fumen_util import unglue_fumen

def unglue(glued):
  if (type(glued) == type([])):
    return unglue_fumen(glued)
  return unglue_fumen([glued])[0]

def system(command):
    print(command)
    ossystem(command)

allpcdata = {}
for i in range(1, 2):
    allpcdata[i] = {}
    allpcdata[i]["data"] = loads(open(f"cover{i}.json").read())
    allpcdata[i]["setups"] = open(f"setups{i}.txt").read().splitlines()
    allpcdata[i]["percent"] = open(f"percent{i}.txt").read().splitlines()

def getbestsetup(allpieces):
    pcnumber = 1
    allsetups = []

    for piecelength in range(3, len(allpieces) + 2):
        testsetup = allpieces[:piecelength]
        if (testsetup in allpcdata[pcnumber]["data"]):
            workingsetups = allpcdata[pcnumber]["data"][testsetup]
            [allsetups.append(i) for i in workingsetups]
    allsetups.sort()
    return [allsetups[0], allpcdata[pcnumber]["percent"][allsetups[0]]]

setups = open("setups1.txt").read().splitlines()
pieces = list(extendPieces(["*p7"]))

endhtml = "First pc website<br>"

for queue in pieces:
    bestsetup, chance = getbestsetup(queue)
    endhtml += f'<a href=setups/{bestsetup}.html>{queue}: {chance}%</a><br>'

landingpage = open("index.html", "w")
landingpage.write(endhtml)
landingpage.close()
