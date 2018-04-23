from numba import jit
import numpy as np
from math import sqrt


@jit(nopython=True)
def matrix_multiply(X, Y):
    """ Matrix multiplication
    Inputs:
      - X: A numpy array of shape (N, M)
      - Y: A numpy array of shape (M, K)
    Output:
      - out: A numpy array of shape (N, K)
    """
    N, M = X.shape
    P = Y.shape[1]
    out = np.zeros((N, P))
    for i in range(N):
        for j in range(P):
            for k in range(M):
                out[i, j] += X[i, k] * Y[k, j]
    return out


@jit(nopython=True)
def matrix_rowmean(X, weights=np.empty(0)):
    """ Calculate mean of each row.
    In case of weights do weighted mean.
    For example, for matrix [[1, 2, 3]] and weights [0, 1, 2]
    weighted mean equals 2.6666 (while ordinary mean equals 2)
    Inputs:
      - X: A numpy array of shape (N, M)
      - weights: A numpy array of shape (M,)
    Output:
      - out: A numpy array of shape (N,)
    """
    N, M = X.shape
    out = np.zeros(N)
    if weights.size <= 0:
        weights = np.ones(M)
    denominator = 0
    for i in range(M):
        denominator += weights[i]
    for i in range(N):
        row_sum = 0
        for j in range(M):
            row_sum += X[i, j] * weights[j]
        out[i] = np.divide(row_sum, denominator)
    return out


@jit(nopython=True)
def matrix_rowstd(X):
    N, M = X.shape
    mean = matrix_rowmean(X)
    out = np.zeros(N)
    for i in range(N):
        var_sum = 0
        for j in range(M):
            var_sum += (X[i, j] - mean[i]) ** 2
        out[i] = sqrt(var_sum / (M))
    return out


@jit(nopython=True)
def matrix_l2_norm(X):
    N, M = X.shape
    out = np.zeros(N)
    for i in range(N):
        row_sum = 0
        for j in range(M):
            row_sum += X[i, j] ** 2
        out[i] = sqrt(row_sum)
    return out.reshape(N, -1)


@jit(nopython=True)
def matrix_bdiv(X, Y):
    N, M = X.shape
    out = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            out[i, j] = X[i, j] / Y[i, j]
    return out


@jit(nopython=True)
def matrix_b_multiply(X, Y):
    N = X.shape[0]
    K = Y.shape[1]
    out = np.zeros((N, K))
    for i in range(N):
        for j in range(K):
            out[i, j] = X[i, 0] * Y[0, j]
    return out


@jit(nopython=False)
def row_argsort(row):
    # it is allowed @ slack
    return np.argsort(row)


@jit(nopython=True)
def matrix_argsort(X):
    N, M = X.shape
    out = np.zeros((N, M), dtype=np.int64)
    for i in range(N):
        sorted_row = row_argsort(X[i])
        for j in range(M):
            out[i, j] = sorted_row[j]
    return out


@jit(nopython=True)
def cosine_similarity(X, top_n=10, with_mean=True, with_std=True):
    """ Calculate cosine similarity between each pair of row.
    1. In case of with_mean: subtract mean of each row from row
    2. In case of with_std: divide each row on it's std
    3. Select top_n best elements in each row or set other to zero.
    4. Compute cosine similarity between each pair of rows.
    Inputs:
      - X: A numpy array of shape (N, M)
      - top_n: int, number of best elements in each row
      - with_mean: bool, in case of subtracting each row's mean
      - with_std: bool, in case of subtracting each row's std
    Output:
      - out: A numpy array of shape (N, N)

    Example (with top_n=1, with_mean=True, with_std=True):
        X = array([[1, 2], [4, 3]])
        after mean and std transform:
        X = array([[-1.,  1.], [ 1., -1.]])
        after top n choice
        X = array([[0.,  1.], [ 1., 0]])
        cosine similarity:
        X = array([[ 1.,  0.], [ 0.,  1.]])

    """
    N, M = X.shape
    if with_mean:
        mean = matrix_rowmean(X)
        for i in range(N):
            for j in range(M):
                X[i, j] = X[i, j] - mean[i]
    if with_std:
        std = matrix_rowstd(X)
        for i in range(N):
            for j in range(M):
                X[i, j] /= std[i]
    if top_n is not None:
        sorted_indexes = matrix_argsort(X)
        for i in range(N):
            for j in range(M - top_n):
                X[i, sorted_indexes[i, j]] = 0
    l2_norm_matrix = matrix_b_multiply(matrix_l2_norm(X), matrix_l2_norm(X).T)
    return matrix_bdiv(matrix_multiply(X, X.T), l2_norm_matrix)
