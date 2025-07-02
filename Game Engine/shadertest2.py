import dearpygui.dearpygui as dpg
import numpy as np

# Configuration
TEXTURE_SIZE = 512

# Initialize Dear PyGui
dpg.create_context()

# Create texture registry
with dpg.texture_registry():
    # Start with a simple blue gradient
    texture_data = np.zeros((TEXTURE_SIZE, TEXTURE_SIZE, 4), dtype=np.float32)
    for x in range(TEXTURE_SIZE):
        for y in range(TEXTURE_SIZE):
            texture_data[y, x, 2] = x / TEXTURE_SIZE  # Blue channel
            texture_data[y, x, 3] = 1.0  # Alpha channel
    dpg.add_raw_texture(TEXTURE_SIZE, TEXTURE_SIZE, texture_data, 
                       format=dpg.mvFormat_Float_rgba, tag="output_texture")

# Create UI
with dpg.window(label="Shader Viewer", width=600, height=600):
    dpg.add_image("output_texture", width=512, height=512)
    dpg.add_text("Status: Running", tag="status_text")

# Animation counter
counter = 0

def update_texture():
    global counter
    counter += 1
    
    try:
        # Create an animated pattern
        texture_data = np.zeros((TEXTURE_SIZE, TEXTURE_SIZE, 4), dtype=np.float32)
        for x in range(TEXTURE_SIZE):
            for y in range(TEXTURE_SIZE):
                # Animate based on counter
                texture_data[y, x, 0] = (np.sin(x/50 + counter/10) + 1)/2  # Red
                texture_data[y, x, 1] = (np.cos(y/50 + counter/10) + 1)/2  # Green
                texture_data[y, x, 3] = 1.0  # Alpha
        
        dpg.set_value("output_texture", texture_data)
        dpg.set_value("status_text", f"Frame: {counter}")
        
    except Exception as e:
        dpg.set_value("status_text", f"Error: {str(e)}")
    
    return update_texture

# Setup viewport
dpg.create_viewport(title="Shader Viewer", width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

# Start rendering
dpg.set_frame_callback(5, update_texture)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()