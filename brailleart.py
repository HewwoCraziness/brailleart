BRAILLE_BASE_CODEPOINT = 0x2800

def braillefromchunk (chunk):
    out = BRAILLE_BASE_CODEPOINT
    # Hex values of a chunk:
    # 1  8
    # 2  10
    # 4  20
    # 40 80
    if chunk[(0, 0)]:
        out += 0x1
    if chunk[(0, 1)]:
        out += 0x2
    if chunk[(0, 2)]:
        out += 0x4
    if chunk[(0, 3)]:
        out += 0x40
    if chunk[(1, 0)]:
        out += 0x8
    if chunk[(1, 1)]:
        out += 0x10
    if chunk[(1, 2)]:
        out += 0x20
    if chunk[(1, 3)]:
        out += 0x80
    return chr (out)

def works (func):
    try:
        func ()
        return True
    except:
        return False

def constant_width_float (infloat):
    return "{:.2f}".format (infloat).rjust (6, ' ')

from PIL import Image

from sys import argv
from os.path import isfile

PERCENT_DISPLAY_DIGITS = 2

if (len (argv) == 3 or len (argv) == 4) and isfile (argv[1]) and works (lambda: float (argv[2])):
    print ("Opening {}...".format (argv[1]))
    img = Image.open (argv[1])
    fixedwidth = round (img.width * float (argv[2]) * 2) # should be twice as wide since chunks are 2 wide x 4 tall
    fixedheight = round (img.height * float (argv[2]))
    print ("Scaling to {}x...".format (argv[2]))
    scaled = img.resize ((fixedwidth * 2, fixedheight * 4), resample = Image.LANCZOS)
    print ("Converting to monochrome...")
    monochrome = scaled.convert ("1")
    print ("Loading into a Python object...")
    data = monochrome.load ()
    chunks = {}
    # chunkwidth = img.width * float (argv[2])
    # chunkheight = img.height * float (argv[2])
    for xchunk in range (fixedwidth):
        print ("Chunking the image... {}% complete\r".format (constant_width_float ((xchunk + 1) / fixedwidth * 100)), end = "")
        for ychunk in range (fixedheight):
            newchunk = {}
            for x in range (2):
                for y in range (4):
                    absx = xchunk * 2 + x
                    absy = ychunk * 4 + y
                    newchunk[(x, y)] = data[absx, absy] == 255
            chunks[(xchunk, ychunk)] = newchunk
    print ("\n", end = "")
    print ("{} chunks total".format (len (chunks.keys ())))
    out = ""
    for y in range (fixedheight):
        print ("Converting chunks to braille... {}% complete\r".format (constant_width_float ((y + 1) / fixedheight * 100)), end = "")
        for x in range (fixedwidth):
            out += braillefromchunk (chunks[(x, y)])
        out += "\n"
    print ("\n", end = "")
    if len (argv) == 4:
        with open (argv[3], "w+") as outfile:
            outfile.write (out)
        print ("Saved to {}".format (argv[3]))
    else:
        print (out)
else:
    print ("usage: {} [image] [width] [height] [optional outfile]".format (argv[0]))
