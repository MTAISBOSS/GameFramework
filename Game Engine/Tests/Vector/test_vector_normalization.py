import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Point import Point
from Vector import Vector

class TestVectorNormalized(unittest.TestCase):
    def test_normalized(self):
        a = Point(3, 4, 0)
        result = Vector.normalized(a)
        self.assertAlmostEqual(result.x, 0.6)
        self.assertAlmostEqual(result.y, 0.8)
        self.assertAlmostEqual(result.z, 0)
if __name__ == '__main__':
    unittest.main()