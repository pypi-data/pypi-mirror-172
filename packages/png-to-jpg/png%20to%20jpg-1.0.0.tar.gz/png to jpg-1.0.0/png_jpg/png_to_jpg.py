#importing the required package
from PIL import Image
import os, sys

class converter:
        
    def png_jpg(self,Image_path,source_path):
        im = Image.open(Image_path)
        bg = Image.new("RGB", im.size, (255,255,255))
        bg.paste(im,im)
        bg.save(source_path)
   


