from Vector import Vector

class Transform:
    def __init__(self):
        self.scale = Vector(1,1,1)
        self.rotation = Vector(0,0,0)
        self.position = Vector(0,0,0)
        

    @classmethod
    def EulerAngle(cls):
        pass

    @classmethod
    def Translate(cls,a=Vector(),b=Vector(),time = 0):
        pass 
        