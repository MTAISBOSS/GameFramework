import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Point import Point
from Vector import Vector

class TestVectorDotProduct(unittest.TestCase):
    def test_dot_product(self):
        a = Point(1, 2, 3)
        b = Point(4, 5, 6)
        result = Vector.dot_product(a, b)
        self.assertEqual(result, 32)
if __name__ == '__main__':
    unittest.main()