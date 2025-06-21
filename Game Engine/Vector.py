from math import sqrt,acos,radians,degrees
from Point import Point

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
    def Zero(cls):
        return Point(0,0,0)
    
    @classmethod
    def Up(cls):
        return Point(0,1,0)
    
    @classmethod
    def Forward(cls):
        return Point(0,0,1)
    
    @classmethod
    def Right(cls):
        return Point(1,0,0)
    
    @classmethod
    def DotProduct(cls,a=Point(),b=Point()):
        '''
        Returns the dot product of two vectors
        '''
        return a.x * b.x + a.y * b.y + a.z * b.z
    
    @classmethod
    def CrossProduct(cls,a=Point(),b=Point()):
        '''
        Returns the cross product of two vectors
        '''
        newVector = Point()
        newVector.x = a.y * b.z + a.z * b.y
        newVector.y = a.z * b.x + a.x * b.z
        newVector.z = a.x * b.y + a.y * b.x
        return newVector

    @classmethod
    def AddVectors(cls,a=Point(),b=Point()):
        '''
        Adds vector a to vector b and returns the answer
        '''
        newVector = Point()
        newVector.x = a.x + b.x
        newVector.y = a.y + b.y
        newVector.z = a.z + b.z
        return newVector
    
    @classmethod
    def Distance(cls,a=Point(),b=Point()):
        '''
        Returns the distance between two vectors
        '''
        distance = sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)
        return distance
    
    @classmethod
    def Magnitude(cls,a=Point()):
        '''
        Returns the length of vector a
        '''
        lenght = sqrt((a.x)**2 + (a.y)**2 + (a.z)**2)
        return lenght
    
    @classmethod
    def Normalized(cls,a=Point()):
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
    def Angle(cls,a=Point(),b=Point(),is_rad = True):
        '''
        Returns the angle between two vectors, is_rad determines the angle in radians else in degrees
        '''
        angle = acos((Vector.DotProduct(a,b)) / (Vector.Magnitude(a) * Vector.Magnitude(b)))
        angle = degrees(angle) if not is_rad else angle
        return angle
    
    @classmethod
    def Lerp(cls,a=Point(),b=Point(),time = 0):
        pass

    @classmethod
    def Project(cls,a=Point(),b=Point(),has_angle = False,angle=0):
        pass 