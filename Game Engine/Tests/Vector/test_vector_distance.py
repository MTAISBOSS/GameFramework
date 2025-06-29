import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from math import sqrt
from Point import Point
from Vector import Vector

class TestVectorDistance(unittest.TestCase):
    def test_distance(self):
        a = Point(1, 2, 3)
        b = Point(4, 6, 8)
        result = Vector.distance(a, b)
        expected = sqrt((1-4)**2 + (2-6)**2 + (3-8)**2)
        self.assertEqual(result, expected)
if __name__ == '__main__':
    unittest.main()