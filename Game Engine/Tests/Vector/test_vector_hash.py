import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Vector import Vector

class TestVectorHash(unittest.TestCase):
    def test_hash(self):
        v = Vector(1, 2, 3)
        self.assertEqual(hash(v), hash(v.vector))
if __name__ == '__main__':
    unittest.main()