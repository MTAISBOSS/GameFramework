from Vector import Vector
from Transform import Transform
from Mesh import Mesh
from dearpygui import dearpygui as dpg

class Cube(Mesh):
    def __init__(self, transform=Transform()):
        super().__init__()
        self.transform = transform
        self.color = (255, 0, 0, 255)
        
        self.points = [
            Vector(1, 1, 1),
            Vector(1, 1, -1),
            Vector(1, -1, 1),
            Vector(1, -1, -1),
            Vector(-1, 1, 1),
            Vector(-1, 1, -1),
            Vector(-1, -1, 1), 
            Vector(-1, -1, -1)  
        ]
    
    def get_connected_points(self):
        return [
            (0, 1), (0, 2), (0, 4),
            (1, 3), (1, 5),
            (2, 3), (2, 6),
            (3, 7),
            (4, 5), (4, 6),
            (5, 7), (6, 7)
        ]
    
    def get_faces(self):
        return [
            (0, 2, 4), (2, 6, 4),
            (1, 3, 5), (3, 7, 5),
            (0, 1, 2), (1, 3, 2),
            (4, 5, 6), (5, 7, 6),
            (0, 1, 4), (1, 5, 4),
            (2, 3, 6), (3, 7, 6)
        ]
    
    def draw(self, parent):
        transformed_points = self.get_transformed_points()
        screen_points = []
        
        for point in transformed_points:
            x = point.x + 400 
            y = point.y + 300
            screen_points.append((x, y))
        
        for face in self.get_faces():
            if len(face) >= 3:
                points = [screen_points[i] for i in face[:3]]
                dpg.draw_triangle(
                    points[0], points[1], points[2],
                    color=(*self.color[:3], 50), 
                    fill=(*self.color[:3], 20),
                    parent=parent
                )
        
        for edge in self.get_connected_points():
            if edge[0] < len(screen_points) and edge[1] < len(screen_points):
                dpg.draw_line(
                    screen_points[edge[0]], screen_points[edge[1]],
                    color=self.color,
                    thickness=1,
                    parent=parent
                )