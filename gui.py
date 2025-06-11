# config_gui.py

import customtkinter
import json
import os

stream_url_result = None  # Global holder for result

def open_config_gui():
    def on_save():
        global stream_url_result
        # Save the stream URL and close the window
        # stream_url_result = url_input.get() or default_url
        stream_url_result = url_input.get().strip() or url_presets[option_menu.get()]
        root.destroy()

    default_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8'


    # Named presets
    url_presets = {
        "Rel Munjul - Purwakarta": 'https://cctv.purwakartakab.go.id/cctv/rel-munjul.m3u8?v=4066696',
        "Klari - Arah Cikampek": 'https://s3klari.qumicon.info:8888/camFix-F2/stream.m3u8',
        "Klari - Arah Pintu Tol Karawang Timur": 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8',
        "Klari - Arah Karawang": 'https://s3klari.qumicon.info:8888/camFix-F1/stream.m3u8',
    }

    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    root = customtkinter.CTk()
    root.geometry("400x180")
    root.title("Enter Stream URL")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=20, fill='both', expand=True)

    label1 = customtkinter.CTkLabel(master=frame, text='Pilih Lokasi CCTV:')
    label1.pack(pady=5)

    option_menu = customtkinter.CTkOptionMenu(master=frame, values=list(url_presets.keys()))
    option_menu.pack(pady=5)
    option_menu.set("Klari - Arah Pintu Tol Karawang Timur")  # Default selection

    label = customtkinter.CTkLabel(master=frame, text='Atau Input Stream URL:')
    label.pack(pady=5, padx=5)

    url_input = customtkinter.CTkEntry(master=frame, placeholder_text='e.g., https://...')
    url_input.pack(pady=5, padx=5)

    save_btn = customtkinter.CTkButton(master=frame, text="Save and Start", command=on_save)
    save_btn.pack(pady=15)

    root.mainloop()

    return stream_url_result or default_url