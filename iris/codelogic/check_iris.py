import gc
import numpy as np
from skimage import util
from iris.codelogic import svd_iris, utils, optimization
from iris.models import Irises
from django.conf import settings

def compare_all_iris(iris_relative_path):
    arr_iris = utils.get_array_image(settings.MEDIA_ROOT, iris_relative_path)
    arr_iris = np.transpose(arr_iris)
    mindistance = np.Infinity
    person = ""
    eye = ""
    if arr_iris is not None:
        persons_iris = Irises.objects.all().iterator()
        for iris in persons_iris:
            identity_min_square_left = svd_iris.get_identity_min_square(iris, 'left')
            identity_min_square_right = svd_iris.get_identity_min_square(iris, 'right')
            distance_left = svd_iris.calculate_distance(identity_min_square_left, arr_iris)
            distance_right = svd_iris.calculate_distance(identity_min_square_right, arr_iris)
            print(iris.name, distance_left, distance_right)
            person, mindistance, eye =  calc_smaller(iris, distance_left, distance_right, mindistance, eye, person)
            del identity_min_square_left
            del identity_min_square_right
            gc.collect()
    return person, mindistance, eye

def optimized_compare_all_iris(iris_relative_path):
    arr_iris = utils.get_array_image(settings.MEDIA_ROOT, iris_relative_path)
    arr_iris = np.transpose(arr_iris)
    mindistance = np.Infinity
    person = ""
    eye = ""
    if arr_iris is not None:
        optimization.is_left_or_rigth(arr_iris)


def calc_smaller(person, distance_left, distance_right, min, prev_eye, prev_name):
    if distance_right < min:
        return person.name, distance_right, 'derecho'
    elif distance_left < min: 
        return person.name, distance_left, 'izquierdo'
    return prev_name, min, prev_eye
    