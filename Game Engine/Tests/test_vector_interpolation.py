import unittest
import sys
import os
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from Vector import Vector
from Point import Point

class TestVectorLerp(unittest.TestCase):
    def setUp(self):
        self.start = Point(0, 0, 0)
        self.end = Point(10, 10, 10)

    def test_lerp_at_start(self):
        """Test lerp at t=0 (should return start point)."""
        result = Vector.lerp(self.start, self.end, 0)
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 0)

    def test_lerp_at_end(self):
        """Test lerp at t=1 (should return end point)."""
        result = Vector.lerp(self.start, self.end, 1)
        self.assertEqual(result.x, 10)
        self.assertEqual(result.y, 10)
        self.assertEqual(result.z, 10)

    def test_lerp_at_midpoint(self):
        """Test lerp at t=0.5 (should return midpoint)."""
        result = Vector.lerp(self.start, self.end, 0.5)
        self.assertEqual(result.x, 5)
        self.assertEqual(result.y, 5)
        self.assertEqual(result.z, 5)

    def test_lerp_past_end(self):
        """Test lerp when t > 1 (should extrapolate beyond end)."""
        result = Vector.lerp(self.start, self.end, 1.5)
        self.assertEqual(result.x, 15)
        self.assertEqual(result.y, 15)
        self.assertEqual(result.z, 15)

    def test_lerp_before_start(self):
        """Test lerp when t < 0 (should extrapolate before start)."""
        result = Vector.lerp(self.start, self.end, -0.5)
        self.assertEqual(result.x, -5)
        self.assertEqual(result.y, -5)
        self.assertEqual(result.z, -5)

    def test_lerp_with_non_point_input(self):
        """Test lerp with invalid input (should raise TypeError)."""
        with self.assertRaises(TypeError):
            Vector.lerp("not_a_point", self.end, 0.5)
        with self.assertRaises(TypeError):
            Vector.lerp(self.start, "not_a_point", 0.5)
        with self.assertRaises(TypeError):
            Vector.lerp(self.start, self.end, "not_a_float")

if __name__ == "__main__":
    unittest.main()