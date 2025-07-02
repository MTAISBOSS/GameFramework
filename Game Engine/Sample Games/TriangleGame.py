import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Vector import Vector
from GameObject import GameObject
from Mesh import Mesh
from Transform import Transform
from Time import Time
from Quaternion import Quaternion
from math import *
from dearpygui import dearpygui as dpg

dpg.create_context()

# Game state

time = Time()
screen_mid_height = 100 / 2
screen_mid_width = 100 / 2

speed = 1000
triangle = GameObject("triangle")
triangle_scale = Vector(5,8,5)
triangle.add_component(Mesh)
triangle.get_component(Mesh).points = [
    Vector(-1, 0, 0) * triangle_scale,
    Vector(1, 0, 0)* triangle_scale,
    Vector(0, 1, 0)* triangle_scale
]
triangle.transform = Transform(triangle_scale,Vector(),Vector(screen_mid_width,screen_mid_height))
triangle_points = triangle.get_component(Mesh).points
direction = Vector()
look_direction = Vector()
mouse_pos = Vector()

projectiles = []
projectile_speed = 800
projectile_radius = 5
projectile_cooldown = 0.3
last_shot_time = 0

##########################################################
# Logic
def apply_transform(points, transform):
    transformed = []
    for p in points:
        scaled = Vector(p.x * transform.local_scale.x, p.y * transform.local_scale.y, p.z * transform.local_scale.z)
        rotated = transform.rotation.rotate_vector(scaled)
        final = rotated + transform.position
        transformed.append(final)
    return transformed

def shoot(dir):
    global last_shot_time
    
    current_time = time.time
    if current_time - last_shot_time < projectile_cooldown:
        return
    
    last_shot_time = current_time
    
    projectile = GameObject("projectile")
    spawn_offset = dir * 15
    spawn_position = triangle.transform.position + spawn_offset
    
    projectile.transform = Transform(
        Vector(1, 1, 1),
        Quaternion.identity(),
        spawn_position
    )
    
    projectile.direction = dir
    projectile.speed = projectile_speed
    projectile.lifetime = 2.0
    projectile.radius = projectile_radius
    
    projectiles.append(projectile)

def update_projectiles():
    global projectiles
    
    to_remove = []
    for i, projectile in enumerate(projectiles):
        projectile.transform.position += projectile.direction * projectile.speed * time.delta_time
        
        projectile.lifetime -= time.delta_time
        if projectile.lifetime <= 0:
            to_remove.append(i)
            continue
        
        pos = projectile.transform.position
        dpg.draw_circle(
            center=(pos.x, pos.y),
            radius=projectile.radius,
            color=(255, 0, 0, 255),
            fill=(255, 0, 0, 255),
            parent="canvas"
        )
    
    for i in sorted(to_remove, reverse=True):
        if i < len(projectiles):
            projectiles.pop(i)

def update():
    global look_direction
    
    dpg.delete_item("canvas", children_only=True)
    
    transformed_points = apply_transform(triangle.get_component(Mesh).points, triangle.transform)
    look_direction = Vector.normalized(mouse_pos - triangle.transform.position)
    angle_rad = atan2(look_direction.y, look_direction.x)
    triangle.transform.rotation = Quaternion.from_euler(0, 0, angle_rad - pi/2)

    dpg.draw_triangle(
        p1=(transformed_points[0].x, transformed_points[0].y),
        p2=(transformed_points[1].x, transformed_points[1].y),
        p3=(transformed_points[2].x, transformed_points[2].y),
        color=(255, 255, 255, 255),
        fill=(255, 255, 255, 255),
        parent="canvas"
    )
    
    update_projectiles()

def handle_input_release(sender, app_data):
    pass

def handle_input(sender, app_data):
    global direction, look_direction
    if app_data == dpg.mvKey_Right or app_data == dpg.mvKey_D:
        direction = Vector(1,0,0)
        triangle.transform.position += direction * speed * time.delta_time 
    elif app_data == dpg.mvKey_Left or app_data == dpg.mvKey_A:
        direction = Vector(-1,0,0)
        triangle.transform.position += direction * speed * time.delta_time 
    elif app_data == dpg.mvKey_Up or app_data == dpg.mvKey_W:
        direction = Vector(0,-1,0)
        triangle.transform.position += direction * speed * time.delta_time 
    elif app_data == dpg.mvKey_Down or app_data == dpg.mvKey_S:
        direction = Vector(0,1,0)
        triangle.transform.position += direction * speed * time.delta_time 
    elif app_data == dpg.mvKey_Spacebar:
        shoot(look_direction)
    
    print(triangle.transform.position)
##########################################################
# Draw
with dpg.window(label="Main Window"):
    with dpg.drawlist(width=600, height=600, tag="canvas"):
        pass
  
dpg.create_viewport(title="Triangle Game", width=600, height=600)

with dpg.handler_registry():
    dpg.add_key_press_handler(callback=handle_input)
    dpg.add_key_release_handler(callback=handle_input_release)

dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    time.update()
    update()
    mouse_pos.x,mouse_pos.y = dpg.get_mouse_pos(local=False)
    dpg.render_dearpygui_frame()

dpg.destroy_context()