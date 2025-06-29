from Transform import Transform
import dearpygui.dearpygui as dpg
import numpy as np
from Vector import Vector
class Mesh:
    def __init__(self):
        self.points = []  # List of Vector objects
        self.transform = Transform()
        self.color = (255, 255, 255, 255)  # Default color
        
    def get_transformed_points(self):
        """Apply all transformations to points"""
        transformed = []
        for point in self.points:
            # Apply scale
            scaled = Vector(
                point.vector.x * self.transform.scale.vector.x,
                point.vector.y * self.transform.scale.vector.y,
                point.vector.z * self.transform.scale.vector.z
            ).vector
            
            # Apply rotation
            if hasattr(self.transform, 'rotation'):
                rot_x = np.array(Vector.get_rotation_matrix_x(self.transform.rotation.vector.x))
                rot_y = np.array(Vector.get_rotation_matrix_y(self.transform.rotation.vector.y))
                rot_z = np.array(Vector.get_rotation_matrix_z(self.transform.rotation.vector.z))
                
                vec = np.array([[scaled.x], [scaled.y], [scaled.z]])
                rotated = rot_z @ rot_y @ rot_x @ vec
                scaled = Vector(rotated[0][0], rotated[1][0], rotated[2][0]).vector
            
            # Apply position
            positioned = Vector(
                scaled.x + self.transform.position.vector.x,
                scaled.y + self.transform.position.vector.y,
                scaled.z + self.transform.position.vector.z
            )
            transformed.append(positioned)
        return transformed
    
    def get_connected_points(self):
        """To be implemented by child classes"""
        return []
    
    def get_faces(self):
        """To be implemented by child classes"""
        return []
    
    def draw(self, parent):
        """Draw the mesh with current transformations"""
        transformed_points = self.get_transformed_points()
        screen_points = []
        
        # Project 3D points to 2D screen space
        for point in transformed_points:
            # Simple orthographic projection (modify for perspective)
            x = point.x + 400  # Center of screen
            y = point.y + 300
            screen_points.append((x, y))
        
        # Draw faces
        for face in self.get_faces():
            if len(face) >= 3:
                points = [screen_points[i] for i in face[:3]]
                dpg.draw_triangle(
                    points[0], points[1], points[2],
                    color=self.color, fill=self.color,
                    parent=parent
                )
        
        # Draw edges
        for edge in self.get_connected_points():
            if edge[0] < len(screen_points) and edge[1] < len(screen_points):
                dpg.draw_line(screen_points[edge[0]], screen_points[edge[1]],color=(0, 0, 0, 255), thickness=1,parent=parent)