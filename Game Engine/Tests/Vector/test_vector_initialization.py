import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Vector import Vector

class TestVectorInit(unittest.TestCase):
    def test_default_init(self):
        v = Vector()
        self.assertEqual(v.vector.x, 0)
        self.assertEqual(v.vector.y, 0)
        self.assertEqual(v.vector.z, 0)
        
    def test_init_with_values(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v.vector.x, 1)
        self.assertEqual(v.vector.y, 2)
        self.assertEqual(v.vector.z, 3)

if __name__ == '__main__':
    unittest.main()