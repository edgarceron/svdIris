import os
import numpy as np
from numpy.core.numeric import identity
from numpy.linalg import svd
from django.conf import settings
from iris.models import Irises

def create_dirs(name, eye, file):
    dirs = os.path.join(settings.MEDIA_ROOT, name)
    os.makedirs(dirs, True) if not os.path.isdir(dirs) else None
    return os.path.join(dirs , file + eye + '.npy')

def calc_svd_iris(iris: Irises, eye: str) -> tuple[np.ndarray, np.ndarray]:
    iris_matrix = get_all_iris(iris, eye)
    avg_iris = get_avg_iris(iris, eye, iris_matrix)
    U = get_svd_iris(iris, eye, iris_matrix, avg_iris)
    return U

def get_all_iris(iris: Irises, eye: str) -> np.ndarray:

    file_name_x = create_dirs(iris.name, eye, 'all')
    arr = get_np_from_file(file_name_x)
    if arr is None:
        if eye == 'left':
            arr = np.transpose(np.array(iris.left))
        else:
            arr = np.transpose(np.array(iris.right))
        np.save(file_name_x, arr)
    return arr

def get_avg_iris(iris: Irises, eye: str, iris_matrix: np.ndarray) -> np.ndarray:
    file_name_avg = create_dirs(iris.name, eye, 'avg')
    avg = get_np_from_file(file_name_avg)
    if avg is None:
        avg = np.mean(iris_matrix, axis=1)
        np.save(file_name_avg, avg)
    return avg

def get_svd_iris(iris: Irises, eye: str, iris_matrix: np.ndarray, avg: np.ndarray) -> np.ndarray:
    file_name_svd =  create_dirs(iris.name, eye, 'svd')
    U = get_np_from_file(file_name_svd)
    if U is None:
        X = iris_matrix - np.tile(avg,(iris_matrix.shape[1],1)).T
        U, S, VT = np.linalg.svd(X,full_matrices=0)
        np.save(file_name_svd, U)
    return U

def get_np_from_file(file_name) -> np.ndarray:
    try:
        arr = np.load(os.path.join(settings.MEDIA_ROOT, settings.MEDIA_ROOT,file_name))
        return arr
    except IOError:
        print("Hubo un error al tratar de leer el archivo {}".format(file_name))
    return None

def get_identity_min_square(iris: Irises, eye: str):
    file_name_square =  create_dirs(iris.name, eye, 'squareu')
    identity_min_square = get_np_from_file(file_name_square)
    if identity_min_square is None:
        U = calc_svd_iris(iris, eye)
        squareU = np.float16(U)
        squareU = np.dot(U, np.transpose(U))
        u_shaped_identity = np.identity(squareU.shape[0], np.float16)
        identity_min_square = u_shaped_identity - squareU
        np.save(file_name_square, identity_min_square)
    return identity_min_square

def calculate_distance(identity_min_square: np.ndarray, z: np.ndarray):
    z = np.float16(z)
    res = np.dot(identity_min_square, z)
    distance = np.linalg.norm(res, 2)
    return distance
