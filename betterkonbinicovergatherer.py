from py_fumen_py import decode
import json
from os import system as ossystem
debug = True
def system(command):
    global lastcommand
    if(debug):
        print(command)
    ossystem(command)

pccoverdata = {}

pc = 2

pcpieces = open(f"konbini/pieces{pc}.txt", "r").read().splitlines()
pcsetups = open(f"konbini/setups{pc}.txt", "r").read().splitlines()

for setupindex, pcsetup in enumerate(pcsetups):
    print(f"On setup {setupindex + 1} of {len(pcsetups)}")
    pcsetupdecoded = decode(pcsetup)
    pieces = pcpieces[setupindex]
    if(pc == 3):
        pieces = pieces[0]
    if(pc == 5):
        pieces = pieces[:2]
    pieces = pieces.replace("	", "")
    howmanypieces = len(pcsetupdecoded) - len(pieces)
    if(pc == 6):
        pieces = f'"[^{pieces[0]}]"!'
    elif(len(pieces) != len(set(pieces))):
        pieces = ",".join([i for i in pieces])
    else:
        pieces = f"[{pieces}]!"
    if(howmanypieces > 0):
        system(f'java -jar sfinder.jar cover --tetfu {pcsetup} -p {pieces},*p{howmanypieces} --kicks kicks/jstris180.properties -d 180 > coverdata.txt')
    else:
        system(f'java -jar sfinder.jar cover --tetfu {pcsetup} -p {pieces} --kicks kicks/jstris180.properties -d 180 > coverdata.txt')
    coverdata = [i.split(",") for i in open("output/cover.csv").read().splitlines()[1:]]
    for cover in coverdata:
        if(cover[1] == "O"):
            if(not cover[0] in pccoverdata):
                pccoverdata[cover[0]] = []
            pccoverdata[cover[0]].append(setupindex)
    if(howmanypieces > 0):
        howmanypieces += 1
        system(f'java -jar sfinder.jar cover --tetfu {pcsetup} -p {pieces},*p{howmanypieces} --kicks kicks/jstris180.properties -d 180 > coverdata.txt')
        coverdata = [i.split(",") for i in open("output/cover.csv").read().splitlines()[1:]]
        for cover in coverdata:
            if(cover[1] == "O"):
                if(not cover[0] in pccoverdata):
                    pccoverdata[cover[0]] = []
                pccoverdata[cover[0]].append(setupindex)

with open(f'konbini/cover{pc}.json', 'w', encoding="utf-8") as f:
    json.dump(pccoverdata, f)
