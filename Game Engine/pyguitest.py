from dearpygui import dearpygui as dpg
from Vector import Vector
from Ethereum import Ethereum
from Cube import Cube
import numpy as np

dpg.create_context()

scale = 100
position = 400
ROTATE_SPEED = 0.01

projection_vector = Vector(1, 1, 0).vector
cube = Cube()
ethereum = Ethereum()

angle_x = angle_y = angle_z = 0


with dpg.theme() as button_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (150, 50, 100), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 80, 150), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 30, 80), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)

with dpg.window(label="Control Panel", width=400, height=400, pos=(0, 0)):
    with dpg.collapsing_header(label="Advanced Settings", default_open=True):
        dpg.add_slider_float(label="Volume", default_value=0.5)

    dpg.add_input_text(label="Notes")
    button = dpg.add_button(label="Click here")
    dpg.bind_item_theme(button, button_theme)

    with dpg.child_window(label="Hierarchy", width=200, height=200, border=True):
        dpg.add_text("Rero rero")

with dpg.window(label="Render", width=800, height=800, pos=(410, 0)):
    dpg.add_drawlist(width=800, height=800, tag="canvas")

def connect_points(i, j, points):
    dpg.draw_line(color=(0, 0, 0, 255), p1=points[i], p2=points[j], parent="canvas")

def draw_face(i, j, k, points):
    dpg.draw_triangle(color=(255, 255, 255, 255), p1=points[i], p2=points[j],p3=points[k], parent="canvas",fill=(255, 255, 255, 255))


def draw_shape():
    global angle_x, angle_y, angle_z
    dpg.delete_item("canvas", children_only=True)

    angle_x += ROTATE_SPEED
    angle_y += ROTATE_SPEED
    angle_z += ROTATE_SPEED

    rot_x = np.array(Vector.get_rotation_matrix_x(angle_x))
    rot_y = np.array(Vector.get_rotation_matrix_y(angle_y))
    rot_z = np.array(Vector.get_rotation_matrix_z(angle_z))

    points = []
    for vector in ethereum.ethereum:
        vec = np.array([[vector.x], [vector.y], [vector.z]])
        rotated = rot_z @ rot_y @ rot_x @ vec

        x = rotated[0][0] * scale + position
        y = rotated[1][0] * scale + position
        dpg.draw_circle(center=(x, y), radius=5, color=(255, 255, 255, 255), parent="canvas")
        points.append((x, y))


    for face in ethereum.get_faces():
        draw_face(face[0],face[1],face[2],points)

    for point in ethereum.get_connected_points():
        connect_points(point[0],point[1],points) 


dpg.create_viewport(title="Enigma", width=1220, height=820)
dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    draw_shape()
    dpg.render_dearpygui_frame()
    
dpg.destroy_context()
