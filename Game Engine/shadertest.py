import dearpygui.dearpygui as dpg
from OpenGL.GL import *
import numpy as np
import ctypes
import time

# Shader Code
vertex_shader = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

fragment_shader = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);  // Orange color
}
"""

# Initialize OpenGL resources
def init_opengl():
    global shader_program, vao, vbo
    
    # Compile shaders
    vertex = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex, vertex_shader)
    glCompileShader(vertex)
    
    fragment = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment, fragment_shader)
    glCompileShader(fragment)
    
    # Create shader program
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex)
    glAttachShader(shader_program, fragment)
    glLinkProgram(shader_program)
    
    # Triangle vertices (NDC coordinates)
    vertices = np.array([
        -0.5, -0.5, 0.0,  # left
         0.5, -0.5, 0.0,  # right
         0.0,  0.5, 0.0   # top
    ], dtype=np.float32)
    
    # Create VAO and VBO
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

# Render to texture
def render_to_texture():
    # Create framebuffer
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    
    # Create texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 512, 512, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)
    
    # Render triangle
    glViewport(0, 0, 512, 512)
    glClearColor(0.2, 0.3, 0.3, 1.0)  # Dark background
    glClear(GL_COLOR_BUFFER_BIT)
    
    glUseProgram(shader_program)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    
    # Read pixels
    texture_data = np.zeros((512, 512, 4), dtype=np.float32)
    glReadPixels(0, 0, 512, 512, GL_RGBA, GL_FLOAT, texture_data)
    
    # Clean up
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteFramebuffers(1, [fbo])
    glDeleteTextures(1, [texture])
    
    return texture_data

# Main Dear PyGui setup
dpg.create_context()

# Create texture registry
with dpg.texture_registry():
    # Initialize with bright red to verify visibility
    initial_texture = np.ones((512, 512, 4), dtype=np.float32)
    initial_texture[:, :, :3] = [1.0, 0.0, 0.0]  # Red
    dpg.add_raw_texture(512, 512, initial_texture, 
                       format=dpg.mvFormat_Float_rgba, tag="opengl_texture")

# Create window
with dpg.window(label="OpenGL Shader Output", width=600, height=600):
    dpg.add_image("opengl_texture", width=512, height=512)

# Initialize OpenGL after viewport is created
def on_viewport_created():
    init_opengl()
    
    def update_texture():
        try:
            texture_data = render_to_texture()
            # Flip vertically (OpenGL renders upside down)
            texture_data = np.flipud(texture_data)
            dpg.set_value("opengl_texture", texture_data)
        except Exception as e:
            print(f"Rendering error: {e}")
        return update_texture  # Return itself to keep running
    
    # Start updating after a short delay
    dpg.set_frame_callback(5, update_texture)

dpg.set_viewport_resize_callback(on_viewport_created)

dpg.create_viewport(title="OpenGL + Dear PyGui", width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

# Debug prints to verify execution
print("Dear PyGui running...")
start_time = time.time()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    # Print periodically to confirm the loop is running
    if time.time() - start_time > 2:
        print("Main loop running...")
        start_time = time.time()

dpg.destroy_context()