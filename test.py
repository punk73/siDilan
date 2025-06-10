import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')


def btnOnClick():
    print('lakhsdflaj')


root = customtkinter.CTk()

root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root, width=300, height=200, fg_color='gray')
frame.pack(pady=20, padx=60, fill='both', expand=True)

label = customtkinter.CTkLabel(master=frame, text='Url')
label.pack(pady=12, padx=10)

urlInput = customtkinter.CTkEntry(master=frame, placeholder_text='input url cctv disini')
urlInput.pack(pady=12, padx=10)

btn = customtkinter.CTkButton(master=frame, text="OK", command=btnOnClick)
btn.pack(pady=12, padx=10)

root.mainloop()