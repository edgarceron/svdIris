import numpy as np
from skimage import util
from iris.codelogic import svd_iris, utils
from iris.models import Irises
from django.conf import settings

def compare_all_iris(iris_relative_path):
    arr_iris = utils.get_array_image(settings.MEDIA_ROOT, iris_relative_path)
    arr_iris = np.transpose(arr_iris)
    mindistance = np.Infinity
    person = ""
    if arr_iris is not None:
        persons_iris = Irises.objects.all().iterator()
        for iris in persons_iris:
            identity_min_square_left = svd_iris.get_identity_min_square(iris, 'left')
            identity_min_square_right = svd_iris.get_identity_min_square(iris, 'right')
            distance_left = svd_iris.calculate_distance(identity_min_square_left, arr_iris)
            distance_right = svd_iris.calculate_distance(identity_min_square_right, arr_iris)
            print(iris.name, distance_left, distance_right)
            smaller = min(distance_left, distance_right)
            person = iris.name if smaller < mindistance else person
            mindistance = smaller if smaller < mindistance else mindistance
    return mindistance, person

