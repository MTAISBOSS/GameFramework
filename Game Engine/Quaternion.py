from Vector import Vector
from math import radians,cos,sin,atan2,sqrt,pi
import numpy as np

class Quaternion:
    def __init__(self, w = 0, x = 0, y = 0,z = 0):
        self.q = np.array([w,x, y, z], dtype=np.float64)

    def __repr__(self):
        return f"Quaternion({self.q[0]:.4f}, {self.q[1]:.4f}, {self.q[2]:.4f}, {self.q[3]:.4f})"

    @property
    def x(self):
        return self.q[1]
    
    @x.setter
    def x(self,value):
        self.q[1] = value

    @property
    def y(self):
        return self.q[2]
    
    @y.setter
    def y(self,value):
        self.q[2] = value
    
    @property
    def z(self):
        return self.q[3]
    
    @z.setter
    def z(self,value):
        self.q[3] = value
    
    @property
    def w(self):
        return self.q[0]
    
    @w.setter
    def w(self,value):
        self.q[0] = value

    def __add__(self, other):
        return Quaternion(*(self.q + other.q))

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            w1, x1, y1, z1 = self.q
            w2, x2, y2, z2 = other.q
            w = w1*w2 - x1*x2 - y1*y2 - z1*z2
            x = w1*x2 + x1*w2 + y1*z2 - z1*y2
            y = w1*y2 - x1*z2 + y1*w2 + z1*x2
            z = w1*z2 + x1*y2 - y1*x2 + z1*w2
            return Quaternion(w, x, y, z)
        elif isinstance(other, (float, int)):
            return Quaternion(*(self.q * other))
        else:
            raise TypeError("Multiplication only supported with Quaternion or scalar.")
        
    def identity():
        return Quaternion(1,0,0,0)
    
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self):
        return np.linalg.norm(self.q)

    def inverse(self):
        n2 = self.norm() ** 2
        if n2 == 0:
            raise ZeroDivisionError("Cannot invert a zero quaternion.")
        return self.conjugate() * (1.0 / n2)

    def normalize(self):
        n = self.norm()
        if n == 0:
            raise ValueError("Cannot normalize a zero quaternion.")
        return Quaternion(*(self.q / n))

    def rotate_vector(self, v):
        """Rotate a 3D vector using this quaternion"""
        vq = Quaternion(0, *v)
        rotated = self * vq * self.inverse()
        return rotated.q[1:]  # return x, y, z

    @staticmethod
    def from_axis_angle(axis, angle_rad):
        axis = np.asarray(axis, dtype=np.float64)
        axis = axis / np.linalg.norm(axis)
        s = np.sin(angle_rad / 2)
        return Quaternion(np.cos(angle_rad / 2), *(s * axis)).normalize()

    @staticmethod
    def from_euler(roll, pitch, yaw):
        """Create quaternion from Euler angles (XYZ order)"""
        cr = np.cos(roll / 2)
        sr = np.sin(roll / 2)
        cp = np.cos(pitch / 2)
        sp = np.sin(pitch / 2)
        cy = np.cos(yaw / 2)
        sy = np.sin(yaw / 2)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return Quaternion(w, x, y, z)

    def to_euler(self):
        """Convert quaternion to Euler angles (XYZ order)"""
        w, x, y, z = self.q

        # Roll (X-axis rotation)
        sinr = 2 * (w * x + y * z)
        cosr = 1 - 2 * (x**2 + y**2)
        roll = np.arctan2(sinr, cosr)

        # Pitch (Y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if np.abs(sinp) >= 1:
            pitch = np.pi/2 * np.sign(sinp)  # use 90° if out of range
        else:
            pitch = np.arcsin(sinp)

        # Yaw (Z-axis rotation)
        siny = 2 * (w * z + x * y)
        cosy = 1 - 2 * (y**2 + z**2)
        yaw = np.arctan2(siny, cosy)

        return roll, pitch, yaw  # in radians

    @staticmethod
    def from_euler_deg(x_deg, y_deg, z_deg):
        """Unity-like: Create quaternion from Euler angles (degrees)"""
        x_rad = np.radians(x_deg)
        y_rad = np.radians(y_deg)
        z_rad = np.radians(z_deg)
        return Quaternion.from_euler(x_rad, y_rad, z_rad)

    def to_euler_deg(self):
        """Unity-like: Convert quaternion to Euler angles in degrees"""
        roll, pitch, yaw = self.to_euler()
        return np.degrees([roll, pitch, yaw])
