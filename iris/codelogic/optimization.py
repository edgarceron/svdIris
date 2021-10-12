
import os, gc
import numpy as np
from numpy.linalg import svd
from iris.models import Irises
from iris.codelogic import utils

#Catch the first queater of the image and return it as a vector
def get_quarter_image(imgarr: np.ndarray):
    imgarr = np.reshape(imgarr, (80, 60))
    result = imgarr[:40,:30]
    return result.flatten()

def get_all_iris_quaters(side):
    file_name_x = utils.create_dirs("all", side, "quearter")
    arr = utils.get_np_from_file(file_name_x)
    if arr is None:
        irises = Irises.objects.all().iterator()
        arr = []
        for i in irises:
            ls = i.left if side else i.right
            for i in ls:
                i = get_quarter_image(np.array(i))
                arr.append(i)
        arr = np.array(arr)
        np.save(file_name_x, arr)
        os.chmod(file_name_x, 777)
    return arr

def get_svd(name, iris_matrix):
    file_name_svd = utils.create_dirs("svd", name, "calc")
    arr = utils.get_np_from_file(file_name_svd)
    if arr is None:
        arr, S, VT = np.linalg.svd(iris_matrix,full_matrices=0)
        np.save(file_name_svd, arr)
        os.chmod(file_name_svd, 777)
    return arr

def get_identity_min_square(U, name):
    file_name_square =  utils.create_dirs("quarter", name, 'squareu')
    identity_min_square = utils.get_np_from_file(file_name_square)
    if identity_min_square is None:
        U = np.float16(U)
        squareU = np.matmul(U, np.transpose(U))
        u_shaped_identity = np.identity(squareU.shape[0], np.float16)
        identity_min_square = np.subtract(u_shaped_identity, squareU)
        np.save(file_name_square, identity_min_square)
        os.chmod(file_name_square, 777)
        del U
        del squareU
        del u_shaped_identity
        gc.collect()
    return identity_min_square

def calculate_distance(identity_min_square: np.ndarray, z: np.ndarray):
    z = np.float16(z)
    res = np.matmul(identity_min_square, z)
    distance = np.linalg.norm(res, 2)
    return distance


def is_left_or_rigth(arr_iris):
    iris_left = get_all_iris_quaters('left')
    svd_left = get_svd('left', iris_left)
    del iris_left
    ims_left = get_identity_min_square(svd_left, 'left')
    del svd_left
    dleft =calculate_distance(ims_left, arr_iris)

    iris_right = get_all_iris_quaters('right')
    svd_right = get_svd('right', iris_right)
    del iris_right
    ims_right = get_identity_min_square(svd_right, 'right')
    del svd_right
    dright= calculate_distance(ims_right, arr_iris)

    print(dleft, dright)
    