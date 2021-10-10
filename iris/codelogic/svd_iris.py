import os
import numpy as np
from numpy.core.numeric import identity
from numpy.linalg import svd
from django.conf import settings
from iris.models import Irises

def calc_svd_iris(iris: Irises, eye: str) -> tuple[np.ndarray, np.ndarray]:
    iris_matrix = get_all_iris(iris, eye)
    avg_iris = get_avg_iris(iris, eye, iris_matrix)
    U = get_svd_iris(iris, eye, iris_matrix, avg_iris)
    return U

def get_all_iris(iris: Irises, eye: str) -> np.ndarray:
    file_name_x = os.path.join(iris.name ,'all' + eye + '.npy')
    arr = get_np_from_file(file_name_x)
    if arr is None:
        if eye == 'left':
            arr = np.transpose(np.array(iris.left))
        else:
            arr = np.transpose(np.array(iris.right))
        arr.save(file_name_x)
    return arr

def get_avg_iris(iris: Irises, eye: str, iris_matrix: np.ndarray) -> np.ndarray:
    file_name_avg = os.path.join(iris.name ,'avg' + eye + '.npy')
    avg = get_np_from_file(file_name_avg)
    if avg is None:
        avg = np.mean(iris_matrix, axis=1)
        avg.save(file_name_avg)
    return avg

def get_svd_iris(iris: Irises, eye: str, iris_matrix: np.ndarray, avg: np.ndarray) -> np.ndarray:
    file_name_svd = os.path.join(iris.name ,'svd' + eye + '.npy')
    U = get_np_from_file(file_name_svd)
    if U is None:
        X = iris_matrix - np.tile(avg,(iris_matrix.shape[1],1)).T
        U, S, VT = np.linalg.svd(X,full_matrices=0)
        U.save(file_name_svd)
    return U

def get_np_from_file(file_name) -> np.ndarray:
    try:
        arr = np.load(os.path.join(settings.MEDIA_ROOT,file_name))
        return arr
    except IOError:
        print("Hubo un error al tratar de leer el archivo {}".format(file_name))
    return None

def calculate_distance(U: np.ndarray, z: np.ndarray):
    squareU = np.dot(U, np.transpose(U))
    identity_min_square = np.identity(squareU.shape[0]) - squareU
    distance = np.dot(identity_min_square, z)
    return distance