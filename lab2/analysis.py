# CSC 349-01, Fall 2023
# Leo Rivera
# Sven Toernqvist

import numpy as np
import timeit
from matplotlib import pyplot as plt
from matrix import LinearMxMultiply, DncMxMultiply, StrassenMxMultiply

problem_set = []
matrix_sizes = list(map(lambda x: 2 ** x, range(1, 10)))


def multiplyMatrices(algorithm, n):
    '''Multiply two zero matrices of `n` size using the specified `algorithm`'''
    a = np.zeros((n, n))
    b = np.zeros((n, n))
    f = {
        'dnc': DncMxMultiply,
        'linear': LinearMxMultiply,
        'strassen': StrassenMxMultiply
    }[algorithm]
    f(a, b)


def graphTimeComplexity():
    '''Creates a graph showing the time complexites of the three algorithms'''
    repeat = 1
    dnc_times = []
    strassen_times = []
    linear_times = []
    for i in range(len(matrix_sizes)):
        size = matrix_sizes[i]
        print(f'n={size}:')

        linear_time = timeit.timeit(stmt=f'multiplyMatrices("linear", {size})',
                                    setup='from __main__ import multiplyMatrices', number=repeat) / repeat
        linear_times.append(linear_time)
        print('linear', linear_time)

        dnc_time = timeit.timeit(stmt=f'multiplyMatrices("dnc", {size})', setup='from __main__ import multiplyMatrices',
                                 number=repeat) / repeat
        dnc_times.append(dnc_time)
        print('dnc', dnc_time)

        strassen_time = timeit.timeit(stmt=f'multiplyMatrices("strassen", {size})',
                                      setup='from __main__ import multiplyMatrices', number=repeat) / repeat
        strassen_times.append(strassen_time)
        print('strassen', strassen_time)

        print()

    line1, = plt.plot(matrix_sizes, dnc_times, label='DNC')
    line2, = plt.plot(matrix_sizes, linear_times, label='Linear')
    line3, = plt.plot(matrix_sizes, strassen_times, label='Strassen')
    plt.ylabel('Time')
    plt.xlabel('Array size')
    plt.legend(handles=[line2, line1, line3])
    plt.show()


if __name__ == '__main__':
    graphTimeComplexity()