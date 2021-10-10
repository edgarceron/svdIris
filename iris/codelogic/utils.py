import os, string
import numpy as np
from typing import Tuple
from PIL import Image
from skimage import io
from skimage.util import img_as_int
from iris.models import Config, Irises

def get_array_image(subfolder, image):
    filename, file_extension = os.path.splitext(image)
    if file_extension == '.jpg':
        imgint = img_as_int(io.imread(image, True))
        print(imgint.shape)
        if imgint.shape == (200, 200):
            return imgint
    return None
