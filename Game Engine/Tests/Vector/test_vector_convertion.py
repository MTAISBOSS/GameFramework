import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Point import Point
from Vector import Vector

class TestVectorConvert(unittest.TestCase):
    def test_convert_to_matrix(self):
        a = Point(1, 2, 3)
        result = Vector.convert_to_matrix(a)
        expected = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        self.assertEqual(result, expected)

    def test_convert_to_vector_list(self):
        a = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        result = Vector.convert_to_vector_list(a)
        expected = [
            [1],
            [2],
            [3]
        ]
        self.assertEqual(result, expected)
if __name__ == '__main__':
    unittest.main()