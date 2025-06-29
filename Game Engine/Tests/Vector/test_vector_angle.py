import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from math import degrees, acos
from Point import Point
from Vector import Vector

class TestVectorAngle(unittest.TestCase):
    def test_angle_radians(self):
        a = Point(1, 0, 0)
        b = Point(0, 1, 0)
        result = Vector.angle(a, b)
        expected = acos(0)
        self.assertAlmostEqual(result, expected)
        
    def test_angle_degrees(self):
        a = Point(1, 0, 0)
        b = Point(0, 1, 0)
        result = Vector.angle(a, b, is_rad=False)
        expected = degrees(acos(0))
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main()