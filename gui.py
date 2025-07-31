# config_gui.py

import customtkinter
import json
import os
from states import load

stream_url_result = None  # Global holder for result
model_choice_result = None

def open_config_gui():
    def on_save():
        global stream_url_result
        global model_choice_result
        # Save the stream URL and close the window
        # stream_url_result = url_input.get() or default_url
        stream_url_result = url_input.get().strip() or url_presets[option_menu.get()]
        model_choice_result = model_selector.get()
        root.destroy()

    default_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8'


    # Named presets
    url_presets = load('cctvs.json')

    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    root = customtkinter.CTk()
    root.geometry("500x500")
    root.title("Enter Stream URL")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill='both', expand=True)

    label1 = customtkinter.CTkLabel(master=frame, text='Pilih Lokasi CCTV:')
    label1.pack(pady=5)

    option_menu = customtkinter.CTkOptionMenu(master=frame, values=list(url_presets.keys()))
    option_menu.pack(pady=5)
    option_menu.set("Terminal Klari HD")  # Default selection

    label = customtkinter.CTkLabel(master=frame, text='Atau Input Stream URL:')
    label.pack(pady=5, padx=5)

    url_input = customtkinter.CTkEntry(master=frame, placeholder_text='e.g., https://...')
    url_input.pack(pady=5, padx=5)

    # --- Model Selection ---
    label_model = customtkinter.CTkLabel(master=frame, text='Pilih Model YOLO:')
    label_model.pack(pady=15)

    model_selector = customtkinter.CTkOptionMenu(
        master=frame,
        values=["yolo11n", "yolo11s", "yolo11m", "yolo11l", "yolo11x"]
    )
    model_selector.pack(pady=5)
    model_selector.set("yolo11n")  # Default


    save_btn = customtkinter.CTkButton(master=frame, text="Save and Start", command=on_save)
    save_btn.pack(pady=15)

    root.mainloop()

    # return stream_url_result or default_url
    return stream_url_result or default_url, model_choice_result or "yolo11n"