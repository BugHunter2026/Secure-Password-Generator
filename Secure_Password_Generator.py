import os
import sys
import customtkinter as ctk
from PIL import Image
import string
import secrets

# --- Hilfsfunktion für externe Dateien (Bilder/Icons) ---
# Diese Funktion ist extrem wichtig, damit die fertige .exe später
# weiß, wo sie das Hintergrundbild und das Icon findet.
def resource_path(relative_path):
    try:
        # PyInstaller erstellt einen temporären Ordner und speichert den Pfad in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Wenn wir in VS Code sind, nimm den normalen Pfad
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# --- Grundeinstellungen ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def generate_password():
    length = int(length_slider.get())
    
    characters = string.ascii_letters
    if switch_numbers.get():
        characters += string.digits
    if switch_symbols.get():
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    password_output.configure(state="normal")
    password_output.delete(0, 'end')
    password_output.insert(0, password)
    password_output.configure(state="readonly")
    
    copy_btn.configure(text="Copy to Clipboard")

def update_length_label(value):
    length_label.configure(text=f"Password Length: {int(value)}")

def copy_to_clipboard():
    password = password_output.get()
    if password:
        app.clipboard_clear()
        app.clipboard_append(password)
        copy_btn.configure(text="Copied! ✔️")

# --- Hauptfenster erstellen ---
app = ctk.CTk()
app.geometry("800x450")
app.title("🛡️ Secure Password Generator")
app.resizable(False, False)

# NEU: Das Fenster-Icon setzen
# iconbitmap() erwartet eine .ico Datei
icon_path = resource_path("icon.ico")
try:
    app.iconbitmap(icon_path)
except Exception:
    pass # Ignorieren, falls das Icon noch nicht existiert

# --- Hintergrundbild (PNG) ---
image_path = resource_path("background.png")
try:
    bg_img_data = Image.open(image_path)
    bg_image = ctk.CTkImage(light_image=bg_img_data, dark_image=bg_img_data, size=(800, 450))
    bg_label = ctk.CTkLabel(app, image=bg_image, text="")
    bg_label.place(relx=0.5, rely=0.5, anchor="center")
except FileNotFoundError:
    print(f"Hinweis: Das Bild wurde unter '{image_path}' nicht gefunden.")

# --- Die Karte (Bedienelemente) ---
main_frame = ctk.CTkFrame(app, width=400, height=380, corner_radius=25, fg_color=("gray90", "gray16"))
main_frame.place(relx=0.3, rely=0.5, anchor="center")

# --- UI Elemente ---
title_label = ctk.CTkLabel(main_frame, text="Password Generator", font=("Segoe UI", 22, "bold"))
title_label.pack(pady=(20, 15))

length_label = ctk.CTkLabel(main_frame, text="Password Length: 16", font=("Segoe UI", 14))
length_label.pack(pady=(5, 0))

length_slider = ctk.CTkSlider(main_frame, from_=8, to=64, number_of_steps=56, command=update_length_label)
length_slider.set(16)
length_slider.pack(pady=(5, 15))

switch_numbers = ctk.CTkSwitch(main_frame, text="Include Numbers", font=("Segoe UI", 14))
switch_numbers.select()
switch_numbers.pack(pady=10)

switch_symbols = ctk.CTkSwitch(main_frame, text="Include Symbols", font=("Segoe UI", 14))
switch_symbols.select()
switch_symbols.pack(pady=10)

generate_btn = ctk.CTkButton(main_frame, text="Generate Password", font=("Segoe UI", 15, "bold"), 
                             corner_radius=10, height=40, command=generate_password)
generate_btn.pack(pady=(15, 10))

password_output = ctk.CTkEntry(main_frame, font=("Consolas", 16), width=300, height=40, 
                               justify="center", state="readonly", corner_radius=8)
password_output.pack(pady=(0, 10))

copy_btn = ctk.CTkButton(main_frame, text="Copy to Clipboard", font=("Segoe UI", 13, "bold"), 
                         corner_radius=10, height=35, width=150, 
                         fg_color="#2b2b2b", hover_color="#404040", command=copy_to_clipboard)
copy_btn.pack(pady=(0, 20))

# --- Programm starten ---
app.mainloop()