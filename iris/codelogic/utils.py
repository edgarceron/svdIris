import os, string
from django.core.exceptions import MultipleObjectsReturned
import numpy as np
from django.conf import settings
from PIL import Image
from skimage import io
from skimage.util import img_as_int
from iris.models import Irises

def get_array_image(subfolder, image):
    filename, file_extension = os.path.splitext(image)
    if file_extension == '.bmp':
        imgobj = Image.open(os.path.join(subfolder, image))
        if imgobj.size == (320, 240):
            imgobj = imgobj.resize((80, 60))
            rsz_image_path = os.path.join(settings.MEDIA_ROOT, filename + "rsz" + file_extension)
            imgobj.save(rsz_image_path)
            imgint = io.imread(rsz_image_path, True)
            return imgint.ravel()
    return None

def check_iris(name):
    try: 
        Irises.objects.get(name=name)
        return False
    except Irises.DoesNotExist:
        return True
