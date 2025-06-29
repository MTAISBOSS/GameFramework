import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Vector import Vector

class TestVectorZero(unittest.TestCase):
    def test_zero(self):
        zero = Vector.zero()
        self.assertEqual(zero.x, 0)
        self.assertEqual(zero.y, 0)
        self.assertEqual(zero.z, 0)
    def test_up(self):
        up = Vector.up()
        self.assertEqual(up.x, 0)
        self.assertEqual(up.y, 1)
        self.assertEqual(up.z, 0)

    def test_forward(self):
        forward = Vector.forward()
        self.assertEqual(forward.x, 0)
        self.assertEqual(forward.y, 0)
        self.assertEqual(forward.z, 1)

    def test_right(self):
        right = Vector.right()
        self.assertEqual(right.x, 1)
        self.assertEqual(right.y, 0)
        self.assertEqual(right.z, 0)
if __name__ == '__main__':
    unittest.main()