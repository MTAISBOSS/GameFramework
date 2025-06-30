from Mesh import Mesh
from Vector import Vector
from dearpygui import dearpygui as dpg

class Grid(Mesh):
    def __init__(self, size=10, divisions=10):
        super().__init__()
        self.color = (100, 100, 100, 255)
        self.size = size
        self.divisions = divisions
        self.spacing = size / divisions
        
    def get_connected_points(self):
        edges = []
        half_size = self.size / 2
        
        for i in range(self.divisions + 1):
            z = -half_size + i * self.spacing
            edges.append((Vector(-half_size, 0, z), Vector(half_size, 0, z)))
        
        for i in range(self.divisions + 1):
            x = -half_size + i * self.spacing
            edges.append((Vector(x, 0, -half_size), Vector(x, 0, half_size)))
        
        return edges
    
    def draw(self, parent, camera):
        edges = self.get_connected_points()
        for edge in edges:
            p1 = camera.project_3d_to_2d((edge[0].x, edge[0].y, edge[0].z))
            p2 = camera.project_3d_to_2d((edge[1].x, edge[1].y, edge[1].z))
            
            is_center = (edge[0].x == 0 or edge[0].z == 0 or 
                        edge[1].x == 0 or edge[1].z == 0)
            thickness = 2 if is_center else 1
            color = (150, 150, 150, 255) if is_center else self.color
            
            dpg.draw_line(p1=p1, p2=p2, color=color, thickness=thickness, parent=parent)