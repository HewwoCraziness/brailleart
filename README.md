# brailleart



## About
brailleart is a Python app to create Unicode Braille art from an image using PIL.


## Dependencies
PIL/Pillow: `pip install pillow`


## Syntax
### GUI mode (new in v0.2)
Open the binary or run the source code with `python brailleart.py`.
You should be able to choose the options listed below.
If an output file is not chosen,
the braille art should be shown in a closeable, copyable popup.

### Command-line mode
`python brailleart.py [image] [scale] [optional outfile]`

image: The filename of the target image.

scale: The factor to scale the image by before processing.

optional outfile: The filename to write the output text to. If no file is specified, the output text is printed to standard output.
