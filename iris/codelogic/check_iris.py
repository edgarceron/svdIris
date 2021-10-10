import numpy as np
from skimage import util
from iris.codelogic import svd_iris, utils
from iris.models import Irises
from django.conf import settings

def compare_all_iris(iris_relative_path):
    arr_iris = utils.get_array_image(settings.MEDIA_ROOT, iris_relative_path)
    arr_iris = np.transpose(arr_iris.flatten())
    mindistance = np.Infinity
    if arr_iris is not None:
        persons_iris = Irises.objects.all().iterator()
        for iris in persons_iris:
            U_left = svd_iris.calc_svd_iris(iris, 'left')
            U_right = svd_iris.calc_svd_iris(iris, 'right')
            distance_left = svd_iris.calculate_distance(U_left, arr_iris)
            distance_right = svd_iris.calculate_distance(U_right, arr_iris)
            smaller = min(distance_left, distance_right)
            mindistance = smaller if smaller < mindistance else mindistance
    return mindistance

