from Point import Point
from math import radians,cos,sin
class Quaternian:
    def __init__(self,angle=0,axis=Point()):
        theta = radians(angle) / 2
        self.w = cos(theta)
        self.axis = Point()
        self.axis.x = axis.x * sin(-theta)
        self.axis.y = axis.y * sin(-theta)
        self.axis.z = axis.z * sin(-theta)