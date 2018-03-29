from __future__ import print_function
import os, sys
from PIL import Image


img = Image.open("color.ppm")

print(img.format, img.size, img.mode)
##The format attribute identifies the source of an image.
##If the image was not read from a file, it is set to None.
##The size attribute is a 2-tuple containing width and height (in pixels).
##The mode attribute defines the number and names of the bands in the image,
##and also the pixel type and depth.
##If the file cannot be opened, an IOError exception is raised.

img.show()
##DAMN!


##size = (128, 128)

##img_pixels =  [(255,128,0),(128,0,255),

##test = Image.new("RGB", size, color=0)
##test.putdata(img_pixels)
##
##test.save("test", format="JPEG")