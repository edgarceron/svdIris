import os
from django.core.management.base import BaseCommand
import numpy as np
from typing import Tuple
from PIL import Image

TRANSFOMS = [
    [(.95, 1), (.05, 0), (0, 0)],
    [(.95, 1), (-.05, 0), (12, 0)],
    [(1, .95), (0, 0), (0, 0)],
    [(1, .90), (0, 0), (0, 10)],
    [(1, .90), (0, 0), (0, 5)],
    [(.90, 1), (0, 0), (5, 0)],
    [(.90, 1), (0, 0), (15, 0)],
    [(.90, 1), (0.01, 0.01), (10, -5)],
    [(.90, 1), (0.01, 0.01), (15, -5)],
]

def create_variations(image_path: str, result_path: str, size=0) -> np.ndarray:
    file_name_extensionless = str(os.path.splitext(image_path)[0])
    itrange = len(TRANSFOMS) if size == 0 or size > len(TRANSFOMS) else size
    for i in range(itrange):
        im = apply_variation(image_path, *TRANSFOMS[i])
        new_image_path = os.path.join(result_path, 'variation' + str(i) + '.bmp')
        os.makedirs(result_path) if not os.path.isdir(result_path) else None
        im.save(new_image_path)

def apply_variation(image_path: str, strecth: Tuple, angle: Tuple, translate: Tuple) -> Image.Image:
    try:
        print(image_path)
        with Image.open(image_path) as im:
            im = im.transform(
                im.size, 
                Image.AFFINE, 
                (
                    strecth[0], 
                    angle[0], 
                    translate[0], 
                    angle[1], 
                    strecth[1], 
                    translate[1]
                ), 
                fillcolor=(255,255,255)
            )
            return im
    except OSError:
        print("cannot convert")
        return None

class Command(BaseCommand):
    help = 'Genera variaciones de la imagen dada'

    def add_arguments(self, parser):
        parser.add_argument('imagen', type=str, help='Ruta de la imagen')
        parser.add_argument('guardar_en', type=str, help='Ruta de la carpeta en donde se guardaran las variaciones')

    def handle(self, *args, **kwargs):
        imagen = kwargs['imagen']
        guardar_en = kwargs['guardar_en']
        create_variations(imagen, guardar_en)
