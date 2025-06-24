from math import sqrt,acos,radians,degrees,cos,sin
from Point import Point
import numpy as np
class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.vector = Point(x,y,z)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.vector + other.vector)
        else:
            raise TypeError("Unsupported operand type(s) for +")
    
    def __mul__(self,other):
        if isinstance(other, Vector):
            return Vector(self.vector * other.vector)
        else:
            raise TypeError("Unsupported operand type(s) for *")
        
    @classmethod
    def zero(cls):
        return Point(0,0,0)
    
    @classmethod
    def up(cls):
        return Point(0,1,0)
    
    @classmethod
    def forward(cls):
        return Point(0,0,1)
    
    @classmethod
    def right(cls):
        return Point(1,0,0)
    
    @classmethod
    def dot_product(cls,a=Point(),b=Point()):
        '''
        Returns the dot product of two vectors
        '''
        return a.x * b.x + a.y * b.y + a.z * b.z
    
    @classmethod
    def cross_product(cls,a=Point(),b=Point()):
        '''
        Returns the cross product of two vectors
        '''
        newVector = Point()
        newVector.x = a.y * b.z - a.z * b.y
        newVector.y = a.z * b.x - a.x * b.z
        newVector.z = a.x * b.y - a.y * b.x
        return newVector

    @classmethod
    def add_vectors(cls,a=Point(),b=Point()):
        '''
        Adds vector a to vector b and returns the answer
        '''
        newVector = Point()
        newVector.x = a.x + b.x
        newVector.y = a.y + b.y
        newVector.z = a.z + b.z
        return newVector
    
    @classmethod
    def distance(cls,a=Point(),b=Point()):
        '''
        Returns the distance between two vectors
        '''
        distance = sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)
        return distance
    
    @classmethod
    def magnitude(cls,a=Point()):
        '''
        Returns the length of vector a
        '''
        lenght = sqrt((a.x)**2 + (a.y)**2 + (a.z)**2)
        return lenght
    
    @classmethod
    def normalized(cls,a=Point()):
        '''
        Returns the normalized vector of vector a
        '''
        lenght = Vector.Magnitude(a)
        normalizedVector = Point()
        normalizedVector.x = a.x / lenght
        normalizedVector.y = a.y / lenght
        normalizedVector.z = a.z / lenght
        return normalizedVector
    
    @classmethod
    def angle(cls,a=Point(),b=Point(),is_rad = True):
        '''
        Returns the angle between two vectors, is_rad determines the angle in radians else in degrees
        '''
        angle = acos((Vector.DotProduct(a,b)) / (Vector.Magnitude(a) * Vector.Magnitude(b)))
        angle = degrees(angle) if not is_rad else angle
        return angle
    
    @classmethod
    def get_rotation_matrix_x(cls,angle = 0):
        '''
        Returns the rotation matrix for x
        '''
        rotation_matrix = []
        rotation_matrix.extend([
            [1,0,0],
            [0,cos(angle),-sin(angle)],
            [0,sin(angle),cos(angle)]
            ])
        return rotation_matrix
    
    @classmethod
    def get_rotation_matrix_y(cls,angle = 0):
        '''
        Returns the rotation matrix for y
        '''
        rotation_matrix = []
        rotation_matrix.extend([
            [cos(angle),0,sin(angle)],
            [0,1,0],
            [-sin(angle),0,cos(angle)]
            ])
        return rotation_matrix
    
    @classmethod
    def get_rotation_matrix_z(cls,angle = 0):
        '''
        Returns the rotation matrix for z
        '''
        rotation_matrix = []
        rotation_matrix.extend([
            [cos(angle),-sin(angle),0],
            [sin(angle),cos(angle),0],
            [0,0,1]
            ])
        return rotation_matrix
    
    @classmethod
    def convert_to_matrix(cls,a=Point()):
        matrix = []
        matrix.extend([
            [a.x],
            [a.y],
            [a.z]
            ])
        return matrix
    
    @classmethod
    def convert_to_vector_list(cls,a):
        matrix = []
        matrix.extend([
            [a[0][0]],
            [a[1][1]],
            [a[2][2]]
            ])
        return matrix
    
    @classmethod
    def multiply_matrix(cls,a,b):
        return np.multiply(a,b)

    @classmethod
    def lerp(cls,a=Point(),b=Point(),time = 0):
        pass

    @classmethod
    def project(cls,a=Point(),b=Point(),has_angle = False,angle=0):
        pass 