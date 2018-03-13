import numpy as np
cimport numpy as np
cimport cython

from libc.math cimport sqrt
from libc.math cimport pow

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_multiply(np.ndarray[np.float_t, ndim=2] X,
                      np.ndarray[np.float_t, ndim=2] Y):
    """ Matrix multiplication
    Inputs:
      - X: A numpy array of shape (N, M)
      - Y: A numpy array of shape (M, K)
    Output:
      - out: A numpy array of shape (N, K)
    """
    cdef Py_ssize_t N = X.shape[0]
    cdef Py_ssize_t M = X.shape[1]
    cdef Py_ssize_t K = Y.shape[0]
    cdef Py_ssize_t P = Y.shape[1]
    cdef Py_ssize_t i = 0;
    cdef Py_ssize_t j = 0;
    cdef Py_ssize_t k = 0;
    cdef np.ndarray[np.float_t, ndim=2] out;
    out = np.zeros((N, P), dtype=np.float64)
    for i in range(N):
        for j in range(P):
            temp = 0
            for k in range(M):
                temp = temp + X[i, k] * Y[k, j]
            out[i, j] = temp
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_rowmean(np.ndarray[np.float_t, ndim=2] X,
                     np.ndarray[np.float_t, ndim=1] weights):
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
    cdef int N = X.shape[0];
    cdef int M = X.shape[1];
    cdef float denominator = 0.0;
    cdef float row_sum = 0.0;
    cdef Py_ssize_t i = 0;
    cdef Py_ssize_t j = 0;
    cdef np.ndarray[np.float64_t, ndim=1] out
    out = np.zeros(N)
    if weights.size <= 0:
        weights = np.ones(M)
    for i in range(M):
        denominator += weights[i]
    for i in range(N):
        row_sum = 0.0
        for j in range(M):
            row_sum += X[i, j] * weights[j]
        out[i] = np.divide(row_sum, denominator)
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_rowstd(np.ndarray[np.float64_t, ndim=2]X):
    cdef int N = X.shape[0];
    cdef int M = X.shape[1];
    cdef Py_ssize_t i = 0;
    cdef Py_ssize_t j = 0;
    cdef float var_sum = 0.0;
    cdef np.ndarray[np.float64_t, ndim=1] out
    cdef np.ndarray[np.float64_t, ndim=1] mean
    mean = matrix_rowmean(X, np.empty(0))
    out = np.zeros(N)
    for i in range(N):
        var_sum = 0.0
        for j in range(M):
            var_sum += pow((X[i, j] - mean[i]), 2)
        out[i] = sqrt(var_sum / M)
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_l2_norm(np.ndarray[np.float64_t, ndim=2]X):
    cdef int N = X.shape[0];
    cdef int M = X.shape[1];
    cdef float row_sum = 0.0;
    cdef Py_ssize_t i = 0;
    cdef Py_ssize_t j = 0;
    cdef np.ndarray[np.float64_t, ndim=1] out
    out = np.zeros(N)
    for i in range(N):
        row_sum = 0.0
        for j in range(M):
            row_sum += pow(X[i, j], 2)
        out[i] = sqrt(row_sum)
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_bdiv(np.ndarray[np.float64_t, ndim=2]X,
                  np.ndarray[np.float64_t, ndim=1]Y):
    cdef Py_ssize_t i = 0;
    cdef Py_ssize_t j = 0;
    cdef int N = X.shape[0];
    cdef int M = X.shape[1];
    cdef np.ndarray[np.float64_t, ndim=2] out
    out = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            out[i, j] = X[i, j] / Y[i]
    return out

cpdef row_argsort(np.ndarray[np.float64_t, ndim=1]row):
    return np.argsort(row).astype(np.float64)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef matrix_argsort(np.ndarray[np.float64_t, ndim=2]X):
    cdef Py_ssize_t i = 0;
    cdef long j = 0;
    cdef int N = X.shape[0];
    cdef int M = X.shape[1];
    cdef np.ndarray[np.float64_t, ndim=2] out
    cdef np.ndarray[np.float64_t, ndim=1] sorted_row
    out = np.zeros((N, M))
    for i in range(N):
        sorted_row = row_argsort(X[i])
        for j in range(M):
            out[i, j] = np.int(sorted_row[j])
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cosine_similarity(np.ndarray[np.float64_t, ndim=2]X,
                        np.int64_t top_n=10,
                        with_mean=True,
                        with_std=True):
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
    cdef Py_ssize_t i = 0;
    cdef Py_ssize_t j = 0;
    cdef int N = X.shape[0];
    cdef int M = X.shape[1];
    cdef np.ndarray[np.float64_t, ndim=2] out
    cdef np.ndarray[np.float64_t, ndim=1] mean
    cdef np.ndarray[np.float64_t, ndim=1] std
    cdef np.ndarray[np.float64_t, ndim=2] sorted_indexes
    with_std=False
    if with_mean:
        mean = matrix_rowmean(X, np.empty(0))
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
                X[int(i), int(sorted_indexes[i, j])] = 0
    out = matrix_bdiv(matrix_multiply(X, X.T), matrix_l2_norm(X))
    return matrix_bdiv(out, matrix_l2_norm(X))
