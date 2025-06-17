import customtkinter as ctk
import json
import os
from multiprocessing import Process

config_path = "config.json"

def load_settings():
    with open(config_path) as f:
        return json.load(f)

def save_settings(updated_settings):
    current_config = load_settings()
    current_config.update(updated_settings)
    with open(config_path, 'w') as f:
        json.dump(current_config, f, indent=4)

def open_gui_window():
    app = ctk.CTk()
    app.title("Settings")
    app.geometry("500x500")

    config = load_settings()

    def save_and_close():
        result = {
            "scale": float(scale_slider.get()),
            "thickness": float(thickness_slider.get()),
            "offset": float(offset_slider.get())
        }
        save_settings(result)
        app.destroy()

    # ctk.CTkLabel(app, text="Scale").pack()
    # scale_slider = ctk.CTkSlider(app, from_=0.1, to=5, number_of_steps=49)
    # scale_slider.set(float(config.get("scale", 1.0)))
    # scale_slider.pack()

    # ctk.CTkLabel(app, text="Thickness").pack()
    # thickness_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=49)
    # thickness_slider.set(float(config.get("thickness", 1.0)))
    # thickness_slider.pack()

    # ctk.CTkLabel(app, text="Offset").pack()
    # offset_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=4)
    # offset_slider.set(float(config.get("offset", 3)))
    # offset_slider.pack()

     # --- SCALE ---
    scale_label = ctk.CTkLabel(app, text="Scale (0.1 - 5)")
    scale_label.pack(pady=(20, 0))
    scale_value = ctk.CTkLabel(app, text="1.0")
    scale_value.pack()
    scale_slider = ctk.CTkSlider(app, from_=0.1, to=5.0, number_of_steps=49)
    scale_slider.set(1.0)
    scale_slider.pack()

    def update_scale(val):
        scale_value.configure(text=f"{float(val):.2f}")

    scale_slider.configure(command=update_scale)

    # --- THICKNESS ---
    thickness_label = ctk.CTkLabel(app, text="Thickness (0.1 - 5)")
    thickness_label.pack(pady=(20, 0))
    thickness_value = ctk.CTkLabel(app, text="1.0")
    thickness_value.pack()
    thickness_slider = ctk.CTkSlider(app, from_=0.1, to=5.0, number_of_steps=49)
    thickness_slider.set(1.0)
    thickness_slider.pack()

    def update_thickness(val):
        thickness_value.configure(text=f"{float(val):.2f}")

    thickness_slider.configure(command=update_thickness)

    # --- OFFSET ---
    offset_label = ctk.CTkLabel(app, text="Offset (1 - 5)")
    offset_label.pack(pady=(20, 0))
    offset_value = ctk.CTkLabel(app, text="1")
    offset_value.pack()
    offset_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=4)
    offset_slider.set(1)
    offset_slider.pack()

    def update_offset(val):
        offset_value.configure(text=f"{int(float(val))}")

    offset_slider.configure(command=update_offset)

    ctk.CTkButton(app, text="Save", command=save_and_close).pack(pady=20)

    app.mainloop()

def open_settings_gui():
    # Run the GUI in a separate process to avoid segfault
    p = Process(target=open_gui_window)
    p.start()
    # return 'bangke'