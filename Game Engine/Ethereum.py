from Vector import Vector
from Transform import Transform
from Mesh import Mesh
from dearpygui import dearpygui as dpg
class Ethereum(Mesh):
    def __init__(self, transform=Transform()):
        super().__init__()
        self.transform = transform
        self.color = (100, 75, 200, 150)
        
        self.points = [
            Vector(1, 0, 1),
            Vector(-1, 0, 1),
            Vector(-1, 0, -1),
            Vector(1, 0, -1),
            Vector(0, 2, 0),
            Vector(0, -2, 0)
        ]
    
    def get_connected_points(self):
        return [
            (0, 1), (0, 3), (0, 4), (0, 5),
            (1, 4), (1, 5), (2, 1), (2, 3),
            (2, 4), (2, 5), (3, 4), (3, 5)
        ]
    
    def get_faces(self):
        return [
            (4, 0, 1), (4, 1, 2), (4, 2, 3), (4, 0, 3),
            (5, 0, 1), (5, 1, 2), (5, 2, 3), (5, 0, 3)
        ]
    
    def draw(self, parent):
        transformed_points = self.get_transformed_points()
        self.screen_points = []
        
        for point in transformed_points:
            x = point.x + 400
            y = point.y + 300
            self.screen_points.append((x, y))
        
        for face in self.get_faces():
            if len(face) >= 3:
                points = [self.screen_points[i] for i in face[:3]]
                dpg.draw_triangle(
                    points[0], points[1], points[2],
                    color=(*self.color[:3], 50), fill=(*self.color[:3], 20),
                    parent=parent
                )
        
        for edge in self.get_connected_points():
            if edge[0] < len(self.screen_points) and edge[1] < len(self.screen_points):
                thickness = 2 if (4 in edge or 5 in edge) else 1
                dpg.draw_line(self.screen_points[edge[0]], self.screen_points[edge[1]],color=(150, 100, 255, 255) if thickness > 1 else self.color,thickness=thickness,parent=parent)