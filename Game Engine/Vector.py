import numpy as np
from math import sqrt, acos, radians, degrees, cos, sin

class Vector(np.ndarray):
    def __new__(cls, x=0, y=0, z=0):
        obj = np.asarray([x, y, z], dtype=np.float32).view(cls)
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None: return
    
    @property
    def x(self):
        return self[0]
    
    @x.setter
    def x(self, value):
        self[0] = value
    
    @property
    def y(self):
        return self[1]
    
    @y.setter
    def y(self, value):
        self[1] = value
    
    @property
    def z(self):
        return self[2]
    
    @z.setter
    def z(self, value):
        self[2] = value

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)
    
    @classmethod
    def up(cls):
        return cls(0, 1, 0)
    
    @classmethod
    def forward(cls):
        return cls(0, 0, 1)
    
    @classmethod
    def right(cls):
        return cls(1, 0, 0)
    

    @classmethod
    def dot_product(cls, a, b):
        return np.dot(a, b)
    
    @classmethod
    def cross_product(cls, a, b):
        return np.cross(a, b)
    
    @classmethod
    def distance(cls, a, b):
        return np.linalg.norm(a - b)
    
    @classmethod
    def magnitude(cls, a):
        min_length = 0.0001
        length = np.linalg.norm(a)
        return max(length, min_length)
    
    @classmethod
    def normalized(cls, a):
        length = cls.magnitude(a)
        return a / length
    
    @classmethod
    def angle(cls, a, b, is_rad=True):
        angle = acos(np.dot(a, b) / (cls.magnitude(a) * cls.magnitude(b)))
        return angle if is_rad else degrees(angle)
    
    @classmethod
    def get_rotation_matrix_x(cls, angle=0):
        return np.array([
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)]
        ])
    
    @classmethod
    def get_rotation_matrix_y(cls, angle=0):
        return np.array([
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ])
    
    @classmethod
    def get_rotation_matrix_z(cls, angle=0):
        return np.array([
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]
        ])
    
    @classmethod
    def lerp(cls, a, b, time=0):
        return a + (b - a) * time
    @classmethod
    def slerp(cls, a, b, time=0):
        a_norm = Vector.normalized(a)
        b_norm = Vector.normalized(b)
        
        cos_theta = Vector.dot(a_norm, b_norm)
        
        if cos_theta > 0.9995:
            return Vector.lerp(a_norm, b_norm, time)
        
        cos_theta = max(-1.0, min(1.0, cos_theta))
        
        theta = acos(cos_theta)
        sin_theta = sin(theta)
        
        wa = sin((1 - time) * theta) / sin_theta
        wb = sin(time * theta) / sin_theta
        
        return (a_norm * wa) + (b_norm * wb)

    @classmethod
    def project(cls, a, b):
        return (np.dot(a, b) / np.dot(b, b)) * b