import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from math import cos, sin, radians

from Vector import Vector

class TestVectorRotationMatrix(unittest.TestCase):
    def test_rotation_matrix_x(self):
        angle = radians(90)
        result = Vector.get_rotation_matrix_x(angle)
        expected = [
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)]
        ]
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(result[i][j], expected[i][j])

    def test_rotation_matrix_y(self):
        angle = radians(90)
        result = Vector.get_rotation_matrix_y(angle)
        expected = [
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ]
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(result[i][j], expected[i][j])

    def test_rotation_matrix_z(self):
        angle = radians(90)
        result = Vector.get_rotation_matrix_z(angle)
        expected = [
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]
        ]
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(result[i][j], expected[i][j])

if __name__ == '__main__':
    unittest.main()