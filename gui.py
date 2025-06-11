# config_gui.py

import customtkinter
import json
import os

stream_url_result = None  # Global holder for result

def open_config_gui():
    def on_save():
        global stream_url_result
        # Save the stream URL and close the window
        stream_url_result = url_input.get() or default_url
        root.destroy()

    default_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8'

    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    root = customtkinter.CTk()
    root.geometry("400x180")
    root.title("Enter Stream URL")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill='both', expand=True)

    label = customtkinter.CTkLabel(master=frame, text='Input Stream URL:')
    label.pack(pady=5, padx=5)

    url_input = customtkinter.CTkEntry(master=frame, placeholder_text='e.g., https://...')
    url_input.pack(pady=5, padx=5)

    save_btn = customtkinter.CTkButton(master=frame, text="Save and Start", command=on_save)
    save_btn.pack(pady=15)

    root.mainloop()

    return stream_url_result or default_url