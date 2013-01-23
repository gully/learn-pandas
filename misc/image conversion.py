#convert a .png image file to a .bmp image file using PIL
from PIL import Image

file_in = "test.png"
img = Image.open(file_in)

file_out = "test2.bmp"
print len(img.split())  # test
if len(img.split()) == 4:
    # prevent IOError: cannot write mode RGBA as BMP
    r, g, b, a = img.split()
    img = Image.merge("RGB", (r, g, b))
    img.save(file_out)
else:
    img.save(file_out)

