from Vector import Vector

class Transform:
    def __init__(self,scale=Vector(1,1,1),rotation = Vector(0,0,0),position = Vector(0,0,0)):
        self.scale = scale
        self.rotation = rotation
        self.position = position
        

    @classmethod
    def euler_angle(cls):
        pass

    @classmethod
    def translate(cls,a=Vector(),b=Vector(),time = 0):
        pass 
        