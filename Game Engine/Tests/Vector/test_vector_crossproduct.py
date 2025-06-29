import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Point import Point
from Vector import Vector

class TestVectorCrossProduct(unittest.TestCase):
    def test_cross_product(self):
        a = Point(1, 0, 0)
        b = Point(0, 1, 0)
        result = Vector.cross_product(a, b)
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 1)
if __name__ == '__main__':
    unittest.main()