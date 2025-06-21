class Point:
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self,other):
        if isinstance(other,Point):
            return Point(other.x + self.x, other.y + self.y, other.z + self.z)
        else:
            return TypeError("Unsupported operand type(s) for +")
    
    def __mul__(self,other):
        if isinstance(other,Point):
            return Point(other.x * self.x, other.y * self.y, other.z * self.z)
        else:
            return TypeError("Unsupported operand type(s) for *")
        
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Point(other * self.x,other * self.y,other * self.z)
        else:
            return TypeError("Unsupported operand type(s) for *")