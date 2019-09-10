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

PERCENT_DISPLAY_DIGITS = 2

def imagetobraille (argv):
    # filename (path), scale (float), outfile (path, optional)
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
        return out

from sys import argv
realargv = argv
from os import sep
from os.path import isfile
from tkinter import Tk, Label, Frame, Button, Entry, Text, StringVar, Toplevel, BOTH, END, NONE
from tkinter.filedialog import askopenfilename, asksaveasfilename

class FileChooser (Frame):
    def __init__ (self, root, onchoose = lambda: None, save = False):
        self.root = root
        self.onchoose = onchoose
        self.save = save
        super (FileChooser, self).__init__ (self.root)
        self.choosebutton = Button (self, text = "Choose File", command = self.choosehandler)
        self.choosebutton.grid (row = 0, column = 0)
        self.choosetextvar = StringVar ()
        self.choosetextvar.set ("No file chosen")
        self.choosetext = Label (self, textvariable = self.choosetextvar)
        self.choosetext.grid (row = 0, column = 1)
        self.filename = None
    def choosehandler (self):
        if self.save:
            filename = asksaveasfilename ()
        else:
            filename = askopenfilename ()
        if filename != "":
            print (filename)
            self.filename = filename
            self.choosetextvar.set (filename.split (sep) [-1])
        else:
            self.filename = None
        self.onchoose ()

class TextViewer (Toplevel):
    def __init__ (self, root, text = "The text keyword argument was not set!"):
        self.root = root
        super (TextViewer, self).__init__ ()
        self.closebutton = Button (self, text = "Close", command = self.close)
        self.closebutton.pack ()
        self.outputtext = Text (self, wrap = NONE)
        self.outputtext.tag_config ("styled", foreground = "#00FF00", background = "#000000")
        self.outputtext.insert (END, text, ("styled"))
        self.outputtext.pack (expand = True, fill = BOTH, padx = (0, 0), pady = (0, 0))
    def close (self):
        self.withdraw ()
        self.root.deiconify ()

class brailleart (Tk):
    global realargv
    def __init__ (self):
        super (brailleart, self).__init__ ()
        self.titleframe = Frame (self)
        self.titleframe.pack ()
        self.titlelabel = Label (self.titleframe, text = "brailleart v0.2, by HewwoCraziness (github.com/HewwoCraziness)")
        self.titlelabel.pack ()
        self.inputchooserframe = Frame (self)
        self.inputchooserframe.pack ()
        self.inputchooserlabel = Label (self.inputchooserframe, text = "Input: ")
        self.inputchooserlabel.grid (row = 0, column = 0)
        self.inputchooser = FileChooser (self.inputchooserframe, save = False)
        self.inputchooser.grid (row = 0, column = 1)
        self.scaleframe = Frame (self)
        self.scaleframe.pack ()
        self.scalelabel = Label (self.scaleframe, text = "Scale: ")
        self.scalelabel.grid (row = 0, column = 0)
        self.scaletextvar = StringVar ()
        self.scaleentry = Entry (self.scaleframe, textvariable = self.scaletextvar)
        self.scaleentry.grid (row = 0, column = 1)
        self.scaleafterlabel = Label (self.scaleframe, text = "x")
        self.scaleafterlabel.grid (row = 0, column = 2)
        self.outputchooserframe = Frame (self)
        self.outputchooserframe.pack ()
        self.outputchooserlabel = Label (self.outputchooserframe, text = "Output (optional): ")
        self.outputchooserlabel.grid (row = 0, column = 0)
        self.outputchooser = FileChooser (self.outputchooserframe, save = True)
        self.outputchooser.grid (row = 0, column = 1)
        self.runframe = Frame (self)
        self.runframe.pack ()
        self.runbutton = Button (self.runframe, text = "Run", command = self.runhandler)
        self.runbutton.pack ()
        self.textviewer = None
    def runhandler (self):
        argv = [realargv[0], self.inputchooser.filename, self.scaletextvar.get ()]
        if self.outputchooser.filename != None:
            argv.append (self.outputchooser.filename)
        out = imagetobraille (argv)
        if out != None:
            print ("self.textviewer is {}".format (self.textviewer))
            if self.textviewer != None:
                print ("kaboom")
                self.textviewer.destroy ()
                self.textviewer = None
            self.textviewer = TextViewer (self, out)
            self.withdraw ()

def verifyargv (argv):
    return (len (argv) == 3 or len (argv) == 4) and isfile (argv[1]) and works (lambda: float (argv[2]))

if len (argv) > 1:
    if verifyargv (argv):
        imagetobraille (argv)
    else:
        print ("usage: {} [image] [scale] [optional outfile]".format (argv[0]))
else:
    brailleart_instance = brailleart ()
    brailleart_instance.mainloop ()
