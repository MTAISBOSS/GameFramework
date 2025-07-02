from Transform import Transform
import dearpygui.dearpygui as dpg
import numpy as np
from Vector import Vector
from Component import Component
class Mesh(Component):
    def __init__(self,gameobject):
        super().__init__(gameobject)
        self.points = []
        self.transform = Transform()
        self.color = (255, 255, 255, 255)
        
    def get_transformed_points(self):
        transformed = []
        for point in self.points:
            scaled = Vector(
                point.x * self.transform.scale.x,
                point.y * self.transform.scale.y,
                point.z * self.transform.scale.z
            )
            
            if hasattr(self.transform, 'rotation'):
                rot_x = np.array(Vector.get_rotation_matrix_x(self.transform.rotation.x))
                rot_y = np.array(Vector.get_rotation_matrix_y(self.transform.rotation.y))
                rot_z = np.array(Vector.get_rotation_matrix_z(self.transform.rotation.z))
                
                vec = np.array([[scaled.x], [scaled.y], [scaled.z]])
                rotated = rot_z @ rot_y @ rot_x @ vec
                scaled = Vector(rotated[0][0], rotated[1][0], rotated[2][0])
            
            positioned = Vector(
                scaled.x + self.transform.position.x,
                scaled.y + self.transform.position.y,
                scaled.z + self.transform.position.z
            )
            transformed.append(positioned)
        return transformed
    
    def get_connected_points(self):
        return []
    
    def get_faces(self):
        return []
    
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
                    color=self.color, fill=self.color,
                    parent=parent
                )
        
        for edge in self.get_connected_points():
            if edge[0] < len(screen_points) and edge[1] < len(screen_points):
                dpg.draw_line(screen_points[edge[0]], screen_points[edge[1]],color=(0, 0, 0, 255), thickness=1,parent=parent)