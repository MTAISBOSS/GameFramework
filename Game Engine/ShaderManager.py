import dearpygui.dearpygui as dpg
from OpenGL.GL import *
import numpy as np
import os
import ctypes
import time

# Configuration
SHADER_DIR = "shaders"
TEXTURE_SIZE = 512
POST_PROCESSING_ENABLED = True

class ShaderManager:
    def __init__(self):
        self.shaders = {}
        self.fbos = {}
        self.textures = {}
        self.vao = None
        self.quad_vbo = None
        self.current_effect = "none"
        self.effects = {
            "bloom": {"shader": None, "params": {"threshold": 0.7, "intensity": 1.5}},
            "color_adjust": {"shader": None, "params": {"brightness": 1.0, "contrast": 1.0, "saturation": 1.0}},
            "chromatic_aberration": {"shader": None, "params": {"offset": 0.005}},
            "none": {"shader": None}
        }
        self._initialized = False
        
    def initialize_gl(self):
        """Must be called after OpenGL context is created"""
        # Create shaders
        self.load_shader("main", "main.vert", "main.frag")
        self.load_shader("bloom", "post.vert", "bloom.frag")
        self.load_shader("color_adjust", "post.vert", "color_adjust.frag")
        self.load_shader("chromatic_aberration", "post.vert", "chromatic.frag")
        
        # Setup framebuffers
        self.setup_framebuffer("main")
        self.setup_framebuffer("post")
        self.init_quad()
        self._initialized = True
        
    def load_shader(self, name, vertex_path, fragment_path):
        try:
            # Read shader files
            vertex_src = ""
            fragment_src = ""
            
            if os.path.exists(os.path.join(SHADER_DIR, vertex_path)):
                with open(os.path.join(SHADER_DIR, vertex_path), 'r') as f:
                    vertex_src = f.read()
            else:
                print(f"Vertex shader not found: {vertex_path}")
                return False
                
            if os.path.exists(os.path.join(SHADER_DIR, fragment_path)):
                with open(os.path.join(SHADER_DIR, fragment_path), 'r') as f:
                    fragment_src = f.read()
            else:
                print(f"Fragment shader not found: {fragment_path}")
                return False
            
            # Create and compile shaders
            vertex = glCreateShader(GL_VERTEX_SHADER)
            glShaderSource(vertex, vertex_src)
            glCompileShader(vertex)
            
            # Check compilation status
            if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
                error = glGetShaderInfoLog(vertex).decode()
                print(f"Vertex shader compilation error ({name}):\n{error}")
                return False
                
            fragment = glCreateShader(GL_FRAGMENT_SHADER)
            glShaderSource(fragment, fragment_src)
            glCompileShader(fragment)
            
            if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
                error = glGetShaderInfoLog(fragment).decode()
                print(f"Fragment shader compilation error ({name}):\n{error}")
                return False
                
            # Create and link program
            program = glCreateProgram()
            glAttachShader(program, vertex)
            glAttachShader(program, fragment)
            glLinkProgram(program)
            
            # Check linking status
            if not glGetProgramiv(program, GL_LINK_STATUS):
                error = glGetProgramInfoLog(program).decode()
                print(f"Shader program linking error ({name}):\n{error}")
                return False
                
            self.shaders[name] = program
            return True
            
        except Exception as e:
            print(f"Error loading shader {name}: {str(e)}")
            return False

    def setup_framebuffer(self, name):
        try:
            fbo = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, fbo)
            
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, TEXTURE_SIZE, TEXTURE_SIZE, 
                        0, GL_RGBA, GL_UNSIGNED_BYTE, None)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)
            
            # Check framebuffer status
            if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
                print(f"Framebuffer {name} not complete!")
                return False
                
            self.fbos[name] = fbo
            self.textures[name] = texture
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            return True
            
        except Exception as e:
            print(f"Error setting up framebuffer {name}: {str(e)}")
            return False

    def init_quad(self):
        try:
            vertices = np.array([
                -1, -1, 0, 0,  # x, y, u, v
                 1, -1, 1, 0,
                 1,  1, 1, 1,
                -1,  1, 0, 1
            ], dtype=np.float32)
            
            self.vao = glGenVertexArrays(1)
            self.quad_vbo = glGenBuffers(1)
            
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.quad_vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            
            # Position attribute
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            
            # Texture coordinate attribute
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * ctypes.sizeof(GLfloat), ctypes.c_void_p(2 * ctypes.sizeof(GLfloat)))
            glEnableVertexAttribArray(1)
            
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            return True
            
        except Exception as e:
            print(f"Error initializing quad: {str(e)}")
            return False

    def render_post_effect(self, input_texture):
        if not self._initialized or not POST_PROCESSING_ENABLED or self.current_effect == "none":
            return input_texture
            
        effect = self.effects[self.current_effect]
        if effect["shader"] is None:
            return input_texture
            
        try:
            # Bind post-processing FBO
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbos["post"])
            glViewport(0, 0, TEXTURE_SIZE, TEXTURE_SIZE)
            glClear(GL_COLOR_BUFFER_BIT)
            
            # Use post-processing shader
            glUseProgram(effect["shader"])
            
            # Set uniforms
            glUniform1i(glGetUniformLocation(effect["shader"], "screenTexture"), 0)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, input_texture)
            
            # Set effect parameters
            for param, value in effect["params"].items():
                location = glGetUniformLocation(effect["shader"], param)
                if location != -1:
                    if isinstance(value, float):
                        glUniform1f(location, value)
                    elif isinstance(value, (list, tuple)) and len(value) == 3:
                        glUniform3f(location, *value)
            
            # Render quad
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            glBindVertexArray(0)
            
            # Return the processed texture
            return self.textures["post"]
            
        except Exception as e:
            print(f"Error in post-processing: {str(e)}")
            return input_texture

    def set_effect(self, effect_name):
        if effect_name in self.effects:
            self.current_effect = effect_name

# Initialize Dear PyGui
dpg.create_context()

# Create texture registry
with dpg.texture_registry():
    initial_tex = np.zeros((TEXTURE_SIZE, TEXTURE_SIZE, 4), dtype=np.float32)
    dpg.add_raw_texture(TEXTURE_SIZE, TEXTURE_SIZE, initial_tex, 
                       format=dpg.mvFormat_Float_rgba, tag="output_texture")

# Create UI
with dpg.window(label="Shader Viewer", width=600, height=700):
    dpg.add_image("output_texture", width=512, height=512, tag="output_image")
    dpg.draw_circle(center=(300,300),radius=50,color=(255,255,255,255),fill=(255,255,255,255))
    dpg.add_text("Debug Info:", tag="debug_text")
    with dpg.collapsing_header(label="Post Processing"):
        dpg.add_combo(["none", "bloom", "color_adjust", "chromatic_aberration"], 
                     label="Effect", default_value="none", tag="effect_combo")
        
        with dpg.group(show=POST_PROCESSING_ENABLED):
            with dpg.collapsing_header(label="Bloom Settings", show=False, tag="bloom_settings"):
                dpg.add_slider_float(label="Threshold", default_value=0.7, min_value=0, max_value=1, tag="bloom_threshold")
                dpg.add_slider_float(label="Intensity", default_value=1.5, min_value=0, max_value=5, tag="bloom_intensity")
            
            with dpg.collapsing_header(label="Color Adjust", show=False, tag="color_adjust_settings"):
                dpg.add_slider_float(label="Brightness", default_value=1.0, min_value=0, max_value=2, tag="brightness")
                dpg.add_slider_float(label="Contrast", default_value=1.0, min_value=0, max_value=2, tag="contrast")
                dpg.add_slider_float(label="Saturation", default_value=1.0, min_value=0, max_value=2, tag="saturation")
            
            with dpg.collapsing_header(label="Chromatic Aberration", show=False, tag="chromatic_settings"):
                dpg.add_slider_float(label="Offset", default_value=0.005, min_value=0, max_value=0.02, tag="chromatic_offset")

# Create shader manager
shader_mgr = ShaderManager()

def update_effect_settings(sender, app_data, user_data):
    effect = dpg.get_value("effect_combo")
    shader_mgr.set_effect(effect)
    
    # Update UI visibility
    dpg.configure_item("bloom_settings", show=(effect == "bloom"))
    dpg.configure_item("color_adjust_settings", show=(effect == "color_adjust"))
    dpg.configure_item("chromatic_settings", show=(effect == "chromatic_aberration"))

def update_effect_params():
    if shader_mgr.current_effect == "bloom":
        shader_mgr.effects["bloom"]["params"]["threshold"] = dpg.get_value("bloom_threshold")
        shader_mgr.effects["bloom"]["params"]["intensity"] = dpg.get_value("bloom_intensity")
    elif shader_mgr.current_effect == "color_adjust":
        shader_mgr.effects["color_adjust"]["params"]["brightness"] = dpg.get_value("brightness")
        shader_mgr.effects["color_adjust"]["params"]["contrast"] = dpg.get_value("contrast")
        shader_mgr.effects["color_adjust"]["params"]["saturation"] = dpg.get_value("saturation")
    elif shader_mgr.current_effect == "chromatic_aberration":
        shader_mgr.effects["chromatic_aberration"]["params"]["offset"] = dpg.get_value("chromatic_offset")

# Set callbacks
dpg.set_item_callback("effect_combo", update_effect_settings)
for item in ["bloom_threshold", "bloom_intensity", "brightness", "contrast", "saturation", "chromatic_offset"]:
    dpg.set_item_callback(item, update_effect_params)

# Setup viewport
dpg.create_viewport(title="Shader Viewer", width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
frame_count = 0
# Initialize OpenGL after viewport is created
def on_viewport_created():
    shader_mgr.initialize_gl()
    
    def update_texture():
        if not glGetString(GL_VERSION):
            dpg.set_value("debug_text", "OpenGL not initialized!")
            return update_texture
        global frame_count
        frame_count += 1
        try:
            dpg.set_value("debug_text", 
                     f"Frame: {frame_count}\n"
                     f"Effect: {shader_mgr.current_effect}\n"
                     f"Initialized: {shader_mgr._initialized}")
            # Create a simple test pattern
            texture_data = np.zeros((TEXTURE_SIZE, TEXTURE_SIZE, 4), dtype=np.float32)
            
            # Create a red gradient from left to right
            for x in range(TEXTURE_SIZE):
                for y in range(TEXTURE_SIZE):
                    texture_data[y, x, 0] = x / TEXTURE_SIZE  # Red channel
                    texture_data[y, x, 3] = 1.0  # Alpha channel
            
            # Update the texture
            dpg.set_value("output_texture", texture_data)
            
        except Exception as e:
            print(f"Rendering error: {e}")
        
        return update_texture

dpg.set_viewport_resize_callback(on_viewport_created)

# Main loop
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()