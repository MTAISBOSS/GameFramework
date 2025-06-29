import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Vector import Vector

class TestVectorAdd(unittest.TestCase):
    def test_add_vectors(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result.x, 5)
        self.assertEqual(result.y, 7)
        self.assertEqual(result.z, 9)
        
    def test_add_invalid_type(self):
        v1 = Vector(1, 2, 3)
        with self.assertRaises(TypeError):
            v1 + "invalid"

if __name__ == '__main__':
    unittest.main()