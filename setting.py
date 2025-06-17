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

    ctk.CTkLabel(app, text="Scale").pack()
    scale_slider = ctk.CTkSlider(app, from_=0.1, to=5, number_of_steps=49)
    scale_slider.set(float(config.get("scale", 1.0)))
    scale_slider.pack()

    ctk.CTkLabel(app, text="Thickness").pack()
    thickness_slider = ctk.CTkSlider(app, from_=0.1, to=5, number_of_steps=49)
    thickness_slider.set(float(config.get("thickness", 1.0)))
    thickness_slider.pack()

    ctk.CTkLabel(app, text="Offset").pack()
    offset_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=4)
    offset_slider.set(float(config.get("offset", 3)))
    offset_slider.pack()

    ctk.CTkButton(app, text="Save", command=save_and_close).pack(pady=20)

    app.mainloop()

def open_settings_gui():
    # Run the GUI in a separate process to avoid segfault
    p = Process(target=open_gui_window)
    p.start()
    # return 'bangke'