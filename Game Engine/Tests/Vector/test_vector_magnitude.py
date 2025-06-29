import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Point import Point
from Vector import Vector

class TestVectorMagnitude(unittest.TestCase):
    def test_magnitude(self):
        a = Point(3, 4, 0)
        result = Vector.magnitude(a)
        self.assertEqual(result, 5)
        
    def test_min_magnitude(self):
        a = Point(0, 0, 0)
        result = Vector.magnitude(a)
        self.assertEqual(result, 0.0001)
if __name__ == '__main__':
    unittest.main()