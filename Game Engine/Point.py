class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Point' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Point' and '{}'".format(type(other).__name__))

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Point' and '{type(other).__name__}'")
    def __rmul__(self, scalar):
        return self.__mul__(scalar)