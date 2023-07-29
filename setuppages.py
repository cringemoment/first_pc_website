from os import system as ossystem, mkdir
from py_fumen_util import unglue_fumen
from py_fumen_py import decode as pydecode
from bs4 import BeautifulSoup
from copy import deepcopy
from PIL import Image

def decode(fumen):
    decode_pages = pydecode(fumen)
    return '\n'.join(decode_pages[0].field.string().splitlines()[:-1])

def toimage(fumen, name):
    board = decode(fumen)
    board = [[i for i in j] for j in board.splitlines()]

    fumenimage = Image.new("RGB", (len(board[0]) * 32, len(board) * 32), "black")

    for rownumber, row in enumerate(board):
        for columnnumber, piece in enumerate(row):
            if (not piece == "_"):
                fumenimage.paste(catimages[piece], (columnnumber * 32, rownumber * 32))

    fumenimage.save(f"assets/{name}.png", format="PNG")

def unglue(glued):
  if (type(glued) == type([])):
    return unglue_fumen(glued)
  return unglue_fumen([glued])[0]

def system(command):
    print(command)
    ossystem(command)

def getpieces(fumen):
    fumen = pydecode(fumen)
    pieces = ""
    for i in fumen:
        pieces += str(i.operation.mino)[-1]
    return pieces

def evaluatesave(save):
    piecessaveindex = {"S": 0, "Z": 0, "O": 3, "J": 1, "L": 1, "I": 4, "T": 6}

    score = 0
    for piece in save:
        score += piecessaveindex[piece]

    if (save.count("J") + save.count("L") % 2 == 0):
        score += 8

    if(len(save) != len(set(save))):
        score -= 8

    return score

catimages = {}
for i in "IOSZJLTX_":
  catimages[i] = Image.open(f"cat images/cat{i}.png")

setups = open("setups1.txt").read().splitlines()
setuppieces = open("pieces1.txt").read().splitlines()

for setupindex, setup in enumerate(setups):
    print(f"On setup {setupindex + 1} of {len(setups)}")
    if(setupindex > 0):
        break

    try:
        mkdir(f"setups/{setupindex}")
    except:
        pass

    pieces = getpieces(setup)

    setup = unglue(setup)
    listedpieces = setuppieces[setupindex]

    sfinderpieces = f'"[^{pieces}]!",*p4'
    if(len(pieces) == 7):
        sfinderpieces = "*p7"

    system(f'java -jar sfinder.jar path -t {setup} -p {sfinderpieces} --kicks jstris180.properties -d 180 --split yes > ezsfinder.txt')

    with open('output/path_unique.html', 'r', encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    solutions = []

    for link in soup.find_all('a')[1:]:
        href = link.get('href')
        if href.startswith('http://fumen.zui.jp/?'):
            pieces = ''.join([i[0] for i in link.get_text().split(' ')])
            solutions.append([href, pieces])

    saves = []
    allpieces = ''.join([i for i in "IOSZJLT" if not i in setuppieces]) + "IOSZJLT"

    if (solutions != []):
        for solution in solutions:
            solutionfumen = solution[0]
            piecesused = solution[1]

            solutionallpieces = [char for char in allpieces.replace(",", "")]
            solutionpiecesused = [char for char in piecesused]
            pieceuseddontremove = deepcopy(piecesused)

            for pieceused in pieceuseddontremove:
                solutionpiecesused.remove(pieceused)
                solutionallpieces.remove(pieceused)

            leftover = solutionallpieces
            saves.append([solutionfumen, leftover, evaluatesave(leftover)])

    saves.sort(key=lambda x: int(x[2]) * -1)
    with open("input/field.txt", "w") as w:
        accum = ""
        for solution in saves:
            accum += solution[0] + "\n"
        w.write(accum)

    system(f"java -jar sfinder.jar cover -p {sfinderpieces} -P yes > ezsfinder.txt")

    endfile = f'<img src = ../assets/{setupindex}.png><br>'

    coverfile = open("output/cover.csv").read().splitlines()
    solutions = coverfile[0].split(",")[1:]

    print("writing solution files")
    for solutionindex, solution in enumerate(solutions):
        solution = unglue(solution)
        toimage(solution, f"{setupindex}_{solutionindex}")
        solutionfile = open(f"setups/{setupindex}/{solutionindex}.html", "w")
        solutionfile.write(f'<img src = ../../assets/{setupindex}_{solutionindex}.png>')
        solutionfile.close()

    print("writing hyperlinks")
    for i in coverfile[1:]:
        i = i.split(",")
        queue = i[0]
        coverdata = i[1:]

        if("O" in coverdata):
            rightsolution = coverdata.index("O")
            endfile += f'<a href=={setupindex}/{rightsolution}.html>{queue}</a><br>'
        else:
            endfile += f'<a href=death.html>{queue}</a><br>'

    htmlfile = open(f"setups/{setupindex}.html", "w")
    htmlfile.write(endfile)
    htmlfile.close()
