from Vector import Vector
from Transform import Transform
from Mesh import Mesh
from dearpygui import dearpygui as dpg
import math

class Sphere(Mesh):
    def __init__(self, transform=Transform(), subdivisions=2, radius=1.0):
        super().__init__()
        self.transform = transform
        self.color = (100, 200, 75, 150)
        self.radius = radius
        self.subdivisions = subdivisions
        
        self.points = []
        self.faces_indices = []
        self._generate_sphere()
    
    def _generate_sphere(self):
        t = (1.0 + math.sqrt(5.0)) / 2.0
        
        self.points = [
            Vector.normalized(Vector(-1,  t,  0)) * self.radius,
            Vector.normalized(Vector( 1,  t,  0)) * self.radius,
            Vector.normalized(Vector(-1, -t,  0)) * self.radius,
            Vector.normalized(Vector( 1, -t,  0)) * self.radius,
            
            Vector.normalized(Vector( 0, -1,  t)) * self.radius,
            Vector.normalized(Vector( 0,  1,  t)) * self.radius,
            Vector.normalized(Vector( 0, -1, -t)) * self.radius,
            Vector.normalized(Vector( 0,  1, -t)) * self.radius,
            
            Vector.normalized(Vector( t,  0, -1)) * self.radius,
            Vector.normalized(Vector( t,  0,  1)) * self.radius,
            Vector.normalized(Vector(-t,  0, -1)) * self.radius,
            Vector.normalized(Vector(-t,  0,  1)) * self.radius
        ]
        
        faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
            (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
            (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
            (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
        ]
        
        for _ in range(self.subdivisions):
            new_faces = []
            for face in faces:
                v1 = self.points[face[0]]
                v2 = self.points[face[1]]
                v3 = self.points[face[2]]
                
                a = Vector.normalized(v1 + v2) * self.radius
                b = Vector.normalized(v2 + v3) * self.radius
                c = Vector.normalized(v3 + v1) * self.radius
                
                idx_a = len(self.points)
                self.points.append(a)
                idx_b = len(self.points)
                self.points.append(b)
                idx_c = len(self.points)
                self.points.append(c)
                
                new_faces.append((face[0], idx_a, idx_c))
                new_faces.append((face[1], idx_b, idx_a))
                new_faces.append((face[2], idx_c, idx_b))
                new_faces.append((idx_a, idx_b, idx_c))
            
            faces = new_faces
        
        self.faces_indices = faces
    
    def get_connected_points(self):
        edges = set()
        for face in self.faces_indices:
            edges.add((min(face[0], face[1]), max(face[0], face[1])))
            edges.add((min(face[1], face[2]), max(face[1], face[2])))
            edges.add((min(face[2], face[0]), max(face[2], face[0])))
        return list(edges)
    
    def get_faces(self):
        return self.faces_indices
    
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
                dpg.draw_line(
                    screen_points[edge[0]], screen_points[edge[1]],
                    color=(150, 200, 100, 255),
                    thickness=1,
                    parent=parent
                )