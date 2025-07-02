from Vector import Vector
from Transform import Transform
from Mesh import Mesh
from dearpygui import dearpygui as dpg
import math

class Cone(Mesh):
    def __init__(self, transform=Transform(), segments=16, height=2.0, radius=1.0):
        super().__init__()
        self.transform = transform
        self.color = (200, 100, 50, 150)
        self.segments = segments
        self.height = height
        self.radius = radius
        
        self.points = []
        self._generate_cone()
    
    def _generate_cone(self):
        apex = Vector(0, self.height, 0)
        self.points.append(apex)
        
        for i in range(self.segments):
            angle = 2 * math.pi * i / self.segments
            x = self.radius * math.cos(angle)
            z = self.radius * math.sin(angle)
            self.points.append(Vector(x, 0, z))
        
        self.points.append(Vector(0, 0, 0))
    
    def get_connected_points(self):
        edges = []
        
        for i in range(1, self.segments + 1):
            edges.append((0, i)) 
        
        for i in range(1, self.segments):
            edges.append((i, i + 1))
        edges.append((self.segments, 1))
        
        center_index = len(self.points) - 1
        for i in range(1, self.segments + 1):
            edges.append((i, center_index))
        
        return edges
    
    def get_faces(self):
        faces = []
        center_index = len(self.points) - 1
        
        for i in range(1, self.segments):
            faces.append((0, i, i + 1)) 
        faces.append((0, self.segments, 1)) 
        
        for i in range(1, self.segments):
            faces.append((center_index, i, i + 1))
        faces.append((center_index, self.segments, 1))
        
        return faces
    
    def draw(self, parent):
        transformed_points = self.get_transformed_points()
        screen_points = []
        
        for point in transformed_points:
            x = point.vector.x + 400
            y = point.vector.y + 300
            screen_points.append((x, y))
        
        for face in self.get_faces():
            if len(face) >= 3:
                points = [screen_points[i] for i in face[:3]]
                dpg.draw_triangle(
                    points[0], points[1], points[2],
                    color=(*self.color[:3], 50), fill=(*self.color[:3], 20),
                    parent=parent
                )
        
        for edge in self.get_connected_points():
            if edge[0] < len(screen_points) and edge[1] < len(screen_points):
                thickness = 2 if edge[0] == 0 else 1
                dpg.draw_line(
                    screen_points[edge[0]], screen_points[edge[1]],
                    color=(255, 150, 100, 255) if thickness > 1 else self.color,
                    thickness=thickness,
                    parent=parent
                )