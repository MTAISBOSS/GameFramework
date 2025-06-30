# main.py
import dearpygui.dearpygui as dpg
from Ethereum import Ethereum
import numpy as np
import math
from Vector import Vector
from Grid import Grid
from TransformCoordinates import TransformCoordinates
class Camera:
    def __init__(self):
        self.position = Vector(0, 0, -5)
        self.target = Vector(0, 0, 0)
        self.up = Vector(0, 1, 0)
        self.fov = 60.0
        self.zoom = 1.0
        self.update_view_matrix()
    
    def update_view_matrix(self):
        forward = Vector.normalized(self.target - self.position)
        right = Vector.normalized(Vector.cross_product(forward, self.up))
        up = Vector.cross_product(right, forward)

        rotation = np.array([
            [right[0], right[1], right[2], 0],
            [up[0], up[1], up[2], 0],
            [-forward[0], -forward[1], -forward[2], 0],
            [0, 0, 0, 1]
        ])
       
        translation = np.array([
            [1, 0, 0, -self.position[0]],
            [0, 1, 0, -self.position[1]],
            [0, 0, 1, -self.position[2]],
            [0, 0, 0, 1]
        ])
        
        self.view_matrix = np.dot(rotation, translation)
    
    def project_3d_to_2d(self, point):
        point_4d = np.array([point[0], point[1], point[2], 1])
        transformed = np.dot(self.view_matrix, point_4d)
        
        if transformed[2] != 0:
            x = transformed[0] / transformed[2] * self.zoom * 100
            y = transformed[1] / transformed[2] * self.zoom * 100
            return (x + 400, y + 300)
        return (0, 0)

def handle_input(sender, app_data):
    move_speed = 0.5
    rotate_speed = 0.1

    if app_data == dpg.mvKey_W:
        camera.position += Vector(0, 0, move_speed)
    elif app_data == dpg.mvKey_S:
        camera.position += Vector(0, 0, -move_speed)
    elif app_data == dpg.mvKey_A:
        camera.position += Vector(-move_speed, 0, 0)
    elif app_data == dpg.mvKey_D:
        camera.position += Vector(move_speed, 0, 0)
    elif app_data == dpg.mvKey_Q:
        camera.position += Vector(0, -move_speed, 0)
    elif app_data == dpg.mvKey_E:
        camera.position += Vector(0, move_speed, 0)
    elif app_data == dpg.mvKey_Left:
        angle = rotate_speed
        rot_y = Vector.get_rotation_matrix_y(angle)
        camera.position = np.dot(rot_y, camera.position)
    elif app_data == dpg.mvKey_Right:
        angle = -rotate_speed
        rot_y = Vector.get_rotation_matrix_y(angle)
        camera.position = np.dot(rot_y, camera.position)
    elif app_data == dpg.mvKey_Z:
        camera.zoom *= 1.1
    elif app_data == dpg.mvKey_X:
        camera.zoom *= 0.9
    
    camera.update_view_matrix()
    update_scene()

dpg.create_context()
dpg.create_viewport(title='Enigma', width=800, height=600)

camera = Camera()
ethereum = Ethereum()
grid = Grid(size=20, divisions=20)
transformCoordinates = TransformCoordinates(ethereum.transform)
ethereum.transform.position = Vector(0, 1, 0)
ethereum.transform.scale = Vector(1, 1, 1)

def update_scene():
    dpg.delete_item("drawing_container", children_only=True)
    grid.draw("drawing_container", camera)
    transformCoordinates.draw("drawing_container",camera)

    transformed_points = ethereum.get_transformed_points()
    screen_points = [camera.project_3d_to_2d(p) for p in transformed_points]
    
    for face in ethereum.get_faces():
        if len(face) >= 3:
            points = [screen_points[i] for i in face[:3]]
            dpg.draw_triangle(*points,
                color=(100, 75, 200, 50), 
                fill=(100, 75, 200, 20),
                parent="drawing_container"
            )
    
    for edge in ethereum.get_connected_points():
        if edge[0] < len(screen_points) and edge[1] < len(screen_points):
            thickness = 2 if (4 in edge or 5 in edge) else 1
            dpg.draw_line(
                screen_points[edge[0]], screen_points[edge[1]],
                color=(150, 100, 255, 255) if thickness > 1 else (100, 75, 200, 255),
                thickness=thickness,
                parent="drawing_container"
            )

# UI Setup
with dpg.window(label="Enigma", width=800, height=600):
    with dpg.drawlist(width=800, height=600, tag="drawing_container"): pass
    with dpg.group():
        dpg.add_text("Camera Controls:")
        dpg.add_text("W/S: Move forward/backward")
        dpg.add_text("A/D: Move left/right")
        dpg.add_text("Q/E: Move up/down")
        dpg.add_text("Arrow Keys: Rotate view")
        dpg.add_text("Z/X: Zoom in/out")

with dpg.handler_registry():
    dpg.add_key_press_handler(callback=handle_input)

update_scene()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()