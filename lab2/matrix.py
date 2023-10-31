# CSC 349-01, Fall 2023
# Leo Rivera
# Sven Toernqvist

import numpy as np


def FindNearestPowerOfTwo(n):
    return 1 << (n - 1).bit_length()


def PadMatrices(a, b) -> tuple[int, int]:
    '''Takes two matrices of any shape and returns two square matrices with dimensions as a power of two'''
    a_shape = a.shape
    b_shape = b.shape
    max_a, min_a = max(a_shape), min(a_shape)
    max_b, min_b = max(b_shape), min(b_shape)
    n = FindNearestPowerOfTwo(max(max_a, max_b))
    if min_a < n:
        new_a = np.zeros((n, n))
        new_a[:a_shape[0], :a_shape[1]] = a
    else:
        new_a = a
    if min_b < n:
        new_b = np.zeros((n, n))
        new_b[:b_shape[0], :b_shape[1]] = b
    else:
        new_b = b
    return (new_a, new_b)


def MatrixSum(a, b):
    '''Returns the element wise sum of two matrices'''
    if type(a) != np.ndarray:
        return a + b
    n = a.shape[0]
    result = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            result[i, j] = a[i, j] + b[i, j]
    return result


def MatrixDiff(a, b):
    '''Returns the element wise difference of two matrices'''
    if type(a) != np.ndarray:
        return a - b
    n = a.shape[0]
    result = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            result[i, j] = a[i][j] - b[i][j]
    return result


def LinearMxMultiply(a, b):
    '''Takes two matrices and returns their product, num_cols of a must match num_rows of b'''
    num_rows_a = len(a)
    num_cols_a = len(a[0])
    num_rows_b = len(b)
    num_cols_b = len(b[0])

    if num_cols_a != num_rows_b:
        raise Exception(f'Matrix shapes are not compatible \na: {np.shape(a)} \nb: {np.shape(b)}')

    result = np.empty((num_rows_a, num_cols_b))

    for i in range(num_rows_a):
        for j in range(num_cols_b):
            sum = 0
            for k in range(num_cols_a):
                sum += a[i, k] * b[k, j]
            result[i, j] = sum
    return result


def DncMxMultiply(a, b):
    '''Takes two matrices, formats them into square 2^k x 2^k matrices, and returns their product'''
    num_rows_a = len(a)
    num_cols_b = len(b[0])
    padded_a, padded_b = PadMatrices(a, b)
    padded_result = MatMulDNC(padded_a, padded_b)
    return padded_result[:num_rows_a, :num_cols_b]


def MatMulDNC(a, b):
    '''Takes two square 2^k x 2^k matrices, and recursively solves their product'''
    n = a.shape[0]

    if n == 1:
        return a[0][0] * b[0][0]

    half = n // 2

    x = a[:half, :half]
    y = a[:half, half:]
    z = a[half:, :half]
    w = a[half:, half:]
    p = b[:half, :half]
    q = b[:half, half:]
    r = b[half:, :half]
    s = b[half:, half:]

    c1 = MatrixSum(MatMulDNC(x, p), MatMulDNC(y, r))
    c2 = MatrixSum(MatMulDNC(x, q), MatMulDNC(y, s))
    c3 = MatrixSum(MatMulDNC(z, p), MatMulDNC(w, r))
    c4 = MatrixSum(MatMulDNC(z, q), MatMulDNC(w, s))

    result = np.empty((n, n))
    result[:half, :half] = c1
    result[:half, half:] = c2
    result[half:, :half] = c3
    result[half:, half:] = c4

    return result


def StrassenMxMultiply(a, b):
    '''Takes two matrices, formats them into square 2^k x 2^k matrices, and returns their product'''
    num_rows_a = len(a)
    num_cols_b = len(b[0])
    padded_a, padded_b = PadMatrices(a, b)
    padded_result = MatMulStrassen(padded_a, padded_b)
    return padded_result[:num_rows_a, :num_cols_b]


def MatMulStrassen(a, b):
    '''Takes two square 2^k x 2^k matrices, and recursively solves their product using Strassen's algoruithm'''
    n = a.shape[0]

    if n == 1:
        return np.array([[a[0, 0] * b[0, 0]]])

    half = n // 2
    x = a[:half, :half]
    y = a[:half, half:]
    z = a[half:, :half]
    w = a[half:, half:]
    p = b[:half, :half]
    q = b[:half, half:]
    r = b[half:, :half]
    s = b[half:, half:]

    p1 = MatMulStrassen(x, MatrixDiff(q, s))
    p2 = MatMulStrassen(MatrixSum(x, y), s)
    p3 = MatMulStrassen(MatrixSum(z, w), p)
    p4 = MatMulStrassen(w, MatrixDiff(r, p))
    p5 = MatMulStrassen(MatrixSum(x, w), MatrixSum(p, s))
    p6 = MatMulStrassen(MatrixDiff(y, w), MatrixSum(r, s))
    p7 = MatMulStrassen(MatrixDiff(x, z), MatrixSum(p, q))

    c11 = MatrixSum(MatrixDiff(MatrixSum(p5, p4), p2), p6)
    c12 = MatrixSum(p1, p2)
    c21 = MatrixSum(p3, p4)
    c22 = MatrixDiff(MatrixSum(p1, p5), MatrixSum(p3, p7))

    result = np.empty((n, n))
    result[:half, :half] = c11
    result[:half, half:] = c12
    result[half:, :half] = c21
    result[half:, half:] = c22

    return result