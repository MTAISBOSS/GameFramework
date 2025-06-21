from math import sqrt


class Physic:
    def __init__(self):
        self.gravity = -9.8
        pass

    @classmethod
    def SetGravity(cls,height=0,time=0.1):
        gravity = height / (2 * (time ** 2))
        return gravity

    @classmethod
    def JumpSpeed(cls,height=0):
        speed = sqrt(2* height* Physic.gravity)
        return speed