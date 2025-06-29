import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Vector import Vector

class TestVectorProjection(unittest.TestCase):
    def setUp(self):
        self.vector_a = Vector(1,2,3)
        self.vector_b = Vector(0,1,-2)
    
    def test_projection_for_vectors(self):
        """Test for two given vector"""
        result = Vector.project(self.vector_a.vector,self.vector_b.vector).vector
        self.assertEqual(round(result.x,1),0)
        self.assertEqual(round(result.y,1),-0.8)
        self.assertEqual(round(result.z,1),1.6)

if __name__ == "__main__":
    unittest.main()
