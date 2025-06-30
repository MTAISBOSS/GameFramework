from Mesh import Mesh
from Vector import Vector
from dearpygui import dearpygui as dpg
from Transform import Transform

class TransformCoordinates(Mesh):
    def __init__(self, transorm = Transform()):
        super().__init__()
        self.x_axis_color = (255, 0, 0, 255)
        self.y_axis_color = (0, 0, 255, 255)
        self.z_axis_color = (0, 255, 0, 255)
        self.transform = transorm
        self.scaler = 4
        
    def get_connected_points(self):
        edges = []
        edges.append([Vector(1,0,0) * self.scaler,Vector(0,0,0)])
        edges.append([Vector(0,1,0)* self.scaler,Vector(0,0,0)])
        edges.append([Vector(0,0,1)* self.scaler,Vector(0,0,0)])
        

        return edges
    
    def draw(self, parent, camera):
        edges = self.get_connected_points()
        
        x_p1 = camera.project_3d_to_2d((edges[0][0].x, edges[0][0].y, edges[0][0].z))
        x_p2 = camera.project_3d_to_2d((edges[0][1].x, edges[0][1].y, edges[0][1].z))
        thickness = 3 
        dpg.draw_line(p1=x_p1, p2=x_p2, color=self.x_axis_color, thickness=thickness, parent=parent)

        y_p1 = camera.project_3d_to_2d((edges[1][0].x, edges[1][0].y, edges[1][0].z))
        y_p2 = camera.project_3d_to_2d((edges[1][1].x, edges[1][1].y, edges[1][1].z))
        thickness = 3 
        dpg.draw_line(p1=y_p1, p2=y_p2, color=self.y_axis_color, thickness=thickness, parent=parent)

        z_p1 = camera.project_3d_to_2d((edges[2][0].x, edges[2][0].y, edges[2][0].z))
        z_p2 = camera.project_3d_to_2d((edges[2][1].x, edges[2][1].y, edges[2][1].z))
        thickness = 3 
        dpg.draw_line(p1=z_p1, p2=z_p2, color=self.z_axis_color, thickness=thickness, parent=parent)