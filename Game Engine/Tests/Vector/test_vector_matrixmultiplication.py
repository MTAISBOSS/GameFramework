import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
from Vector import Vector

class TestVectorMultiplyMatrix(unittest.TestCase):
    def test_multiply_matrix(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        result = Vector.multiply_matrix(a, b)
        expected = np.multiply(a, b)
        np.testing.assert_array_equal(result, expected)
if __name__ == '__main__':
    unittest.main()