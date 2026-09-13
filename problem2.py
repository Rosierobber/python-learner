# image distortion Pipeline for VLM  Robustness 
"""generate the 10 image conditions used in the study foir ONE 
in put image 
1 clean + 3 singel distortion + 6 sequyentialk two step combination
DIstortion used :
1 JPEG Compresion 
2  Guassian  BLur
3 Guassian Noise
Usage 
ptython image_ distortion.py path/to/ image /output+folder


**
import io
import os
import sys 
import numpy as np
from PIL import Image, ImageFilter
#  individual distortion functions
# __________________________

def apply_jpeg_compression(img: IMage.Image,quality: int =15)-> Image.Image:
    """