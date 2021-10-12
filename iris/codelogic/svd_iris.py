import os
import gc
import numpy as np
from typing import Tuple
from numpy.core.numeric import identity
from numpy.linalg import svd
from django.conf import settings
from iris.models import Irises
from iris.codelogic import utils



def calc_svd_iris(iris: Irises, eye: str) -> Tuple[np.ndarray, np.ndarray]:
    iris_matrix = get_all_iris(iris, eye)
    avg_iris = get_avg_iris(iris, eye, iris_matrix)
    U = get_svd_iris(iris, eye, iris_matrix, avg_iris)
    return U

def get_all_iris(iris: Irises, eye: str) -> np.ndarray:
    file_name_x = utils.create_dirs(iris.name, eye, 'all')
    arr = utils.get_np_from_file(file_name_x)
    if arr is None:
        if eye == 'left':
            arr = np.transpose(np.array(iris.left))
        else:
            arr = np.transpose(np.array(iris.right))
        np.save(file_name_x, arr)
        os.chmod(file_name_x, 777)
    return arr

def get_avg_iris(iris: Irises, eye: str, iris_matrix: np.ndarray) -> np.ndarray:
    file_name_avg = utils.create_dirs(iris.name, eye, 'avg')
    avg = utils.get_np_from_file(file_name_avg)
    if avg is None:
        avg = np.mean(iris_matrix, axis=1)
        np.save(file_name_avg, avg)
        os.chmod(file_name_avg, 777)
    return avg

def get_svd_iris(iris: Irises, eye: str, iris_matrix: np.ndarray, avg: np.ndarray) -> np.ndarray:
    file_name_svd =  utils.create_dirs(iris.name, eye, 'svd')
    U = utils.get_np_from_file(file_name_svd)
    if U is None:
        #X = iris_matrix - np.tile(avg,(iris_matrix.shape[1],1)).T
        U, S, VT = np.linalg.svd(iris_matrix,full_matrices=0)
        np.save(file_name_svd, U)
        os.chmod(file_name_svd, 777)

    return U



def get_identity_min_square(iris: Irises, eye: str):
    file_name_square =  utils.create_dirs(iris.name, eye, 'squareu')
    identity_min_square = utils.get_np_from_file(file_name_square)
    if identity_min_square is None:
        U = calc_svd_iris(iris, eye)
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
