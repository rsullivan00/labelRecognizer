from munkres import Munkres, print_matrix
import numpy as np


def test(matrix):
    m = Munkres()
    indexes = m.compute(matrix)
    print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        print('(%d, %d) -> %d' % (row, column, value))
    print('total cost: %d' % total)

matrix = [[5, 9, 1, 6],
          [10, 3, 2, 12],
          [8, 7, 4, 11]]
test(matrix)

matrix = [[5, 9],
          [10, 3],
          [8, 7]]
test(matrix)

matrix = np.ones((2, 3)) * 6
matrix[1, 1] = 2
matrix[1, 2] = 5

test(matrix)
