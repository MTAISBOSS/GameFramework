import dearpygui.dearpygui as dpg

dpg.create_context()


with dpg.window(tag="Primary Window",label="Enigma"):
    game_engine_name = dpg.add_text("Enigma Game Engine")
    
    
dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()