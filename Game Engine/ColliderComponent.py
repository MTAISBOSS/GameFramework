from Component import Component
class ColliderComponent(Component):
    def __init__(self, gameobject):
        super().__init__(gameobject)
        self.colliding_with = []

    def get_rect(self,is_2D = True):
        x = self.gameobject.transform.position.vector.x
        y = self.gameobject.transform.position.vector.y
        z = self.gameobject.transform.position.vector.z
        
        h = self.gameobject.transform.scale.vector.x
        w = self.gameobject.transform.scale.vector.y
        d = self.gameobject.transform.scale.vector.z

        result = (x-(w/2),y-(h/2),x+(w/2),y+(h/2)) if is_2D else (x-(w/2),y-(h/2),z-(d/2),x+(w/2),y+(h/2),z+(d/2))
        return result
    
    def check_collision_with(self,other,is_2D = True):
        a = self.get_rect()
        b = other.get_rect()
        
        result = not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3]) if is_2D else not (a[3] < b[0] or a[0] > b[3] or a[4] < b[1] or a[1] > b[4] or a[2] < b[5] or a[5] > b[2])
        return result

    def check_all_collisions(self,colliders):
        self.colliding_with = []
        for other in colliders:
            if other is not self and self.check_collision_with(other):
                self.colliding_with.append(other)