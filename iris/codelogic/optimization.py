
import os, gc, math
import numpy as np
from numpy.lib.arraysetops import intersect1d
from numpy.linalg import svd
from iris.models import Irises
from iris.codelogic import utils

#Catch the first queater of the image and return it as a vector
def get_quarter_image(imgarr: np.ndarray, quarter=0) -> np.ndarray:
    imgarr = np.reshape(imgarr, (80, 60))
    if quarter == 0:
        result = imgarr[:40,:30]
    elif quarter == 1:
        result = imgarr[40:,:30]
    elif quarter == 2:
        result = imgarr[:40,30:]
    else:
        result = imgarr[40:,30:]
    print(result.shape)
    return result.flatten()

def get_all_iris_quaters(side : str) -> np.ndarray:
    file_name_x = utils.create_dirs("all", side, "quearter")
    arr = utils.get_np_from_file(file_name_x)
    if arr is None:
        irises = Irises.objects.all().iterator()
        arr = []
        for iris in irises:
            got = get_irises_quarter_person(iris, side)
            for a in got:
                arr.append(a)
        arr = np.array(arr).transpose()
        np.save(file_name_x, arr)
        os.chmod(file_name_x, 777)
    return arr

def get_irises_quarter_person(iris, side, quarter=0):
    file_name = utils.create_dirs(iris.name, side + str(quarter), "quarters")
    irises_quarter_person = utils.get_np_from_file(file_name)
    if irises_quarter_person is None:
        ls = iris.left if side == 'left' else iris.right
        irises_quarter_person = []
        for i in ls:
            i = get_quarter_image(np.array(i))
            irises_quarter_person.append(i)
        irises_quarter_person = np.array(irises_quarter_person)
        file_name = utils.create_dirs(iris.name, side + str(quarter), "quarters")
        np.save(file_name, irises_quarter_person)
    return irises_quarter_person

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

def calculate_distance(identity_min_square: np.ndarray, z: np.ndarray) -> np.float64:
    z = np.float16(z)
    res = np.matmul(identity_min_square, z)
    distance = np.linalg.norm(res, 2)
    return distance


def is_left_or_rigth(arr_iris):
    iris_left = get_all_iris_quaters('left')
    svd_left = get_svd('left', iris_left)
    ims_left = get_identity_min_square(svd_left, 'left')
    del svd_left
    dleft =calculate_distance(ims_left, arr_iris)

    iris_right = get_all_iris_quaters('right')
    svd_right = get_svd('right', iris_right)
    ims_right = get_identity_min_square(svd_right, 'right')
    del svd_right
    dright= calculate_distance(ims_right, arr_iris)

    r = 'left' if dleft<dright else 'right'
    d = dleft if dleft<dright else dright
    return r, d

def get_irises_from_db(side, quarter):
    file_name_lid =  utils.create_dirs("divisions", side + str(quarter), 'ids')
    lid = utils.get_np_from_file(file_name_lid)
    file_name_l =  utils.create_dirs("divisions", side + str(quarter), 'division')
    l = utils.get_np_from_file(file_name_l)
    iterator = Irises.objects.all().iterator()

    if l is None or lid is None:
        lid = []
        l = []
        for i in iterator:
            lid.append(i.id)
            aux = get_irises_quarter_person(i, side, quarter)
            l.append(aux)
    return l, lid

def start_sort_irises(side, tolerance, z, quarter=0):
    l = None
    lid = None
    quarter = 0
    while len(l) > 1 or quarter < 4:
        oldlid = lid
        lid, l = get_irises_from_db(side, quarter)
        lid, l = sort_irises(lid, l, tolerance, z, side + "q" + str(quarter))
        if oldlid is not None:
            newlid = []
            for i in range(len(l)):
                if l[i] in oldlid:
                    newlid.append(lid[i])
            lid = newlid
        quarter += 1
    return lid

def sort_irises(id_list: list, quarter_list: list, tolerance: int, z: np.ndarray, n: str) -> list:
    l = len(id_list)
    if l == 0:
        return [], []
    else:
        file_name_lid =  utils.create_dirs("divisions", n , 'ids')
        file_name_l =  utils.create_dirs("divisions", n , 'division')
        quarter_2d = []

        for i in quarter_list:
            for j in i:
                quarter_2d.append(j)
        quarter_2d = np.array(quarter_2d)

        np.save(file_name_lid, id_list)
        np.save(file_name_l, quarter_list)

        svd = get_svd("div" + n, np.array(quarter_2d).transpose())
        ims = get_identity_min_square(svd, "idlog" + n)
        distance = calculate_distance(ims, z)
        print(id_list, distance, tolerance, n)
        if distance <= tolerance or distance < 2.5:
            if l == 1:
                return id_list, quarter_list
            firstmidid, firstmid = load_mids(n + "1")
            secondmidid, secondmid = load_mids(n + "2")
            if firstmidid is None or secondmidid is None:
                mid = math.floor(l / 2)
                cont = 0
                firstmidid = []
                firstmid = []
                secondmidid = []
                secondmid = []
                for i in range(l):
                    if cont < mid:
                        firstmidid.append(id_list[i])
                        firstmid.append(quarter_list[i])
                    else:
                        secondmidid.append(id_list[i])
                        secondmid.append(quarter_list[i])
                    cont += 1
            sid1, sidq1 = sort_irises(firstmidid, firstmid, distance, z, n + "1")
            sid2, sidq2 = sort_irises(secondmidid, secondmid, distance, z, n + "2")
            sid1 = list(sid1)
            sid2 = list(sid2)
            sidq1 = list(sidq1)
            sidq2 = list(sidq2)
            return sid1 + sid2, sidq1 + sidq2
        return [], []
          
def load_mids(n):
    file_firstmidid, file_firstmid = file_names(n)
    firstmidid = utils.get_np_from_file(file_firstmidid)
    firstmid = utils.get_np_from_file(file_firstmid)
    return firstmidid, firstmid


def file_names(n): 
    file_firstmidid =  utils.create_dirs("divisions", n, 'ids')
    file_firstmid =  utils.create_dirs("divisions", n, 'division')
    return file_firstmidid, file_firstmid
