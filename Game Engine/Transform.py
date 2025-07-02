from Quaternion import Quaternion  # your implemented class
from Vector import Vector
import numpy as np

class Transform:
    def __init__(self, scale=Vector(1, 1, 1), rotation=Vector(0, 0, 0), position=Vector(0, 0, 0)):
        self.local_position = position
        self.local_scale = scale

        self._eulerAngles = rotation
        self._rotation = Quaternion.from_euler_deg(rotation.x, rotation.y, rotation.z)

    @property
    def position(self):
        return self.local_position

    @position.setter
    def position(self, value):
        self.local_position = value

    @property
    def eulerAngles(self):
        return self._eulerAngles

    @eulerAngles.setter
    def eulerAngles(self, value):
        self._eulerAngles = value
        self._rotation = Quaternion.from_euler_deg(value.x, value.y, value.z)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, quat):
        self._rotation = quat
        x, y, z = quat.to_euler_deg()
        self._eulerAngles = Vector(x, y, z)
        
    def rotate(self, axis, angle_deg):
        """Rotate the transform around axis by angle (in degrees)"""
        delta_q = Quaternion.from_axis_angle(axis, np.radians(angle_deg))
        self.rotation = self.rotation * delta_q  # applies and updates Euler

    def translate(self, delta: Vector):
        """Moves the position by delta (local space)"""
        self.local_position += delta
