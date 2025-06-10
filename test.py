import customtkinter
import json
import os

# UI Appearance
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

# Load from JSON
def load_config():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                url_input.insert(0, config.get("url", ""))
                scale_input.insert(0, config.get("scale", ""))
                thickness_input.insert(0, config.get("thickness", ""))
                offset_input.insert(0, config.get("offset", ""))
            print("Config loaded successfully.")
        except Exception as e:
            print("Error loading config:", e)

# Save function
def btnOnClick():
    data = {
        "url": url_input.get(),
        "scale": scale_input.get(),
        "thickness": thickness_input.get(),
        "offset": offset_input.get()
    }

    try:
        with open("config.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("Config saved to config.json:", data)
    except Exception as e:
        print("Error saving config:", e)


# Main window
root = customtkinter.CTk()
root.geometry("500x400")
root.title("Input Configurator")

py = 5
px = 3

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill='both', expand=True)

# URL
url_label = customtkinter.CTkLabel(master=frame, text='URL')
url_label.pack(pady=py, padx=px)
url_input = customtkinter.CTkEntry(master=frame, placeholder_text='Input URL CCTV')
url_input.pack(pady=py, padx=px)

# Scale
scale_label = customtkinter.CTkLabel(master=frame, text='Scale')
scale_label.pack(pady=py, padx=px)
scale_input = customtkinter.CTkEntry(master=frame, placeholder_text='e.g. 1.0')
scale_input.pack(pady=py, padx=px)

# Thickness
thickness_label = customtkinter.CTkLabel(master=frame, text='Thickness')
thickness_label.pack(pady=py, padx=px)
thickness_input = customtkinter.CTkEntry(master=frame, placeholder_text='e.g. 2')
thickness_input.pack(pady=py, padx=px)

# Offset
offset_label = customtkinter.CTkLabel(master=frame, text='Offset')
offset_label.pack(pady=py, padx=px)
offset_input = customtkinter.CTkEntry(master=frame, placeholder_text='e.g. 10')
offset_input.pack(pady=py, padx=px)

# Save Button
save_btn = customtkinter.CTkButton(master=frame, text="Save", command=btnOnClick)
save_btn.pack(pady=15)


# Load config if exists
load_config()
root.mainloop()