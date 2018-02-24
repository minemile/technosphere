import numpy as np
from scipy.spatial import distance

def first(size):
    """Создать "шахматную доску" на numpy"""
    matrix = np.zeros((size, size))
    matrix[::2, ::2] = 1
    matrix[1::2, 1::2] = 1
    return matrix

def second(size):
    """Создать случайный вектор и занулить три самых больших по модулю значения"""
    rand_vector = np.random.randint(-100, 100, size)
    sort_indexes = np.argsort(np.absolute(rand_vector))
    rand_vector[sort_indexes[-3:]] = 0
    return rand_vector

def third(size):
    """Диагональная матрица с квадратами натуральных чисел"""
    return np.diag(np.arange(1, size + 1) ** 2)

def fouth(size):
    """Змейка"""
    return np.arange(1, size**2+1).reshape(size, size).transpose()

def fifth(size):
    """Евклидово расстояние между вектором и всеми строчками матрицы"""
    vector = np.random.randint(1, 100, size)
    matrix = np.random.randint(1, 100, (size+1, size))
    return np.linalg.norm(matrix - vector, axis=1).reshape(size+1, 1)

def sixth(size):
    """Косинусное расстояние между вектором и всеми строчками матрицы"""
    vector = np.random.randint(1, 100, size)
    matrix = np.random.randint(1, 100, (size+1, size))
    return distance.cdist(matrix, vector.reshape(1, size), 'cosine')

if __name__ == "__main__":
    first(5)
    second(5)
    third(5)
    fouth(5)
    fifth(5)
    sixth(5)
