from Component import Component
from Vector import Vector
from Mesh import Mesh
from math import inf
class SATCollider(Component):
    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.colliding_with = []
    
    def check_collision_with(self,a = Mesh(),b = Mesh()):
        for shape in range(2):
            if shape == 1:
                a,b = b,a

            for i in range(0,len(a.points)):
                first_point = a.points[i]
                second_point = a.points[i+1 % len(a.points)] 
                norm = Vector(-(first_point.y - second_point.y),(first_point.x - second_point.x))

                min_r1 = inf
                max_r1 = -inf
                for p in range(0,len(a.points)):
                    dot = Vector.dot_product(a.points[p],norm.vector)
                    min_r1 = min(min_r1,dot)
                    max_r1 = max(max_r1,dot)

                min_r2 = inf
                max_r2 = -inf
                for p in range(0,len(b.points)):
                    dot = Vector.dot_product(b.points[p],norm.vector)
                    min_r2 = min(min_r2,dot)
                    max_r2 = max(max_r2,dot)

                if not (max_r2 >= min_r1 and max_r1 >= min_r1):
                    return False
            
        return True
    