from py_fumen_py import decode as pydecode
from py_fumen_util import unglue_fumen
from PIL import Image

def decode(fumen):
    decode_pages = pydecode(fumen)
    return '\n'.join(decode_pages[0].field.string().splitlines()[:-1])

def unglue(glued):
  if (type(glued) == type([])):
    return unglue_fumen(glued)
  return unglue_fumen([glued])[0]

catimages = {}
for i in "IOSZJLTX_":
  catimages[i] = Image.open(f"cat images/cat{i}.png")

def toimage(fumen, name):
    board = decode(fumen)
    board = [[i for i in j] for j in board.splitlines()]

    fumenimage = Image.new("RGB", (len(board[0]) * 32, len(board) * 32), "black")

    for rownumber, row in enumerate(board):
        for columnnumber, piece in enumerate(row):
            if (not piece == "_"):
                fumenimage.paste(catimages[piece], (columnnumber * 32, rownumber * 32))

    fumenimage.save(f"assets/{name}.png", format="PNG")

setups = open("setups1.txt").read().splitlines()
for setupindex, setup in enumerate(setups):
    setup = unglue(setup)
    toimage(setup, setupindex)
