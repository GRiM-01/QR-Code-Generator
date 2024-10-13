import tkinter as tk
from tkinter import messagebox
import os
import sys
import pyqrcode as qr
import customtkinter as ctk
from PIL import Image, ImageDraw

# Colours
DARK_BACKGROUND = '#031430'
BUTTON_BACKGROUND = '#2d3f69'
FOREGROUND = '#EFEFFF'
ENTRY_FIELD_BACKGROUND = '#3C4D5E'

# Font
font_name = 'Verdana'
font_size = 12

#Functions
def get_script_directory():
    return os.path.dirname(sys.argv[0])

script_directory = get_script_directory()


def save_qr(name, png_folder, svg_folder):

    qr_type = str(int(slider_type.get()))

    if qr_type == "0":
    
        if not name:
            name = "QR_blank_name_"

            png_name = f"{name}"

            count = 1

            while os.path.exists(os.path.join(png_folder, f"{png_name}.png")):
                png_name = f"{name}_{count}"
                count += 1
        
        else:
            png_name = name

        url_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

        return png_name
    
    elif qr_type == "1":

        if not name:
            name = "QR_blank_name_"

            svg_name = f"{name}"

            count = 1

            while os.path.exists(os.path.join(svg_folder, f"{svg_name}.svg")):
                svg_name = f"{name}_{count}"
                count += 1
        
        else:
            svg_name = name

        url_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)   

        return svg_name

    else:
        print(qr_type)     


def qr_code(url_entry, name_entry):

    qr_type = str(int(slider_type.get()))

    url_str = url_entry.get()
    url = error_correct(url_str)
    name = name_entry.get()

    subfolder_name = 'PNGs'
    png_folder = os.path.join(script_directory, subfolder_name)
    os.makedirs(png_folder, exist_ok=True)

    svg_subfolder_name = 'SVGs'
    svg_folder = os.path.join(script_directory, svg_subfolder_name)
    os.makedirs(svg_folder, exist_ok=True)

    if qr_type == "0":

        png_name = save_qr(name, png_folder, svg_folder)
        png_path = os.path.abspath(os.path.join(png_folder, f'{png_name}.png'))
        url.png(png_path, scale=5)

        rounded_qr = add_rounded_corners(png_path, 25)
        rounded_qr.save(png_path)

        url_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

        os.system(f'start "" "{png_path}"')

    elif qr_type == "1":
        
        svg_name = save_qr(name, png_folder, svg_folder)
        svg_path = os.path.abspath(os.path.join(svg_folder, f'{svg_name}.svg'))
        url.svg(svg_path, scale=5)

        url_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

        os.system(f'start "" "{svg_path}"')    

    else:
        print(qr_type)


def add_rounded_corners(image_path, corner_radius):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        (0, 0, width, height), radius=corner_radius, fill=255
    )

    rounded_img = Image.new("RGBA", img.size)
    rounded_img.paste(img, (0, 0), mask)

    return rounded_img

    
def quit_application():
    confirm_quit = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if confirm_quit:
        root.destroy()


def show_help():
    help_message = "Enter your URL and a Name for the QR code into the entry boxes." + '\n' + "Select a value on the first slider for error correction and redundancy." + '\n' + "The slider at the bottom can be used to toggle between PNG (default) and svg save modes." + '\n' + "Finally, press enter to create your QR code." + '\n''\n' + 'Note*' +'\n''\n'+ "Higher redundancy leads to bigger QR codes, which due to increased error protection, may require more space and hold less data, leading to slower scanning and potential compatibility issues with some scanners." + '\n''\n' "However, lower levels of redundacy may make the QR codes more susceptible to errors or damage, which can lead to difficulties in scanning and retrieving accurate data."
    messagebox.showinfo("Help", help_message)


def map_err_to_labels(value):
    levels = ["0", "L = 7%", "M = 15%", "Q = 25%", "H = 30%"]
    index = int(value)
    return levels[index]

def map_type_to_labels(value):
    levels = ["PNG", "SVG"]
    index = int(value)
    return levels[index]

def slider_err_event(value):
    slider_err_label.configure(text=map_err_to_labels(value))
    return value

def slider_type_event(value):
    slider_type_label.configure(text=map_type_to_labels(value))
    return value


def error_correct(url_str):

    err = str(int(slider_err.get()))

    if err == '1':
        err = 'L'

        url = qr.create(url_str, error = err)

    elif err == '2':
        err = 'M'

        url = qr.create(url_str, error = err)

    elif err == '3':
        err = 'Q'

        url = qr.create(url_str, error = err)

    elif err == '4':
        err = 'H'
        
        url = qr.create(url_str, error = err)

    else:
        url = qr.create(url_str)
 
    return url


# Main
if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("400x300")
    root.resizable(False, False)
    root.title("QR Code Generator")
    root.iconbitmap("myIcon.ico")
    root.configure(bg=DARK_BACKGROUND)

    slider_err = ctk.CTkSlider(master=root,
                                 from_ = 0,
                                 to = 4,
                                 number_of_steps = 4,
                                 width = 280, 
                                 height = 16,
                                 border_width = 5.5,
                                 fg_color='#EFEFFF', 
                                 progress_color='#3C4D7E',
                                 button_color='#3C4D7E',
                                 button_hover_color='#3C4DCE',
                                 command=slider_err_event)
    slider_err.set(1)
    slider_err.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    slider_err_label = ctk.CTkLabel(master=root, text='', font=(font_name, font_size))
    slider_err_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    slider_type = ctk.CTkSlider(master=root,
                                 from_ = 0,
                                 to = 1,
                                 number_of_steps = 1,
                                 width = 60, 
                                 height = 16,
                                 border_width = 5.5,
                                 fg_color='#3C4D7E', 
                                 progress_color='#3C4D7E',
                                 button_color='#3C4D7E',
                                 button_hover_color='#3C4DCE',
                                 command=slider_type_event)
    slider_type.set(0)
    slider_type.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    slider_type_label = ctk.CTkLabel(master=root, text='', font=(font_name, font_size))
    slider_type_label.place(relx=0.5, rely=0.92, anchor=tk.CENTER)

    url_frame = tk.Frame(root, bg = DARK_BACKGROUND)  
    url_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    url_label = tk.Label(url_frame, text="URL:", font=(font_name, font_size), bg = DARK_BACKGROUND, fg = FOREGROUND,)  # Dark background, white text
    url_label.pack(side=tk.LEFT, padx=10)

    url_entry = tk.Entry(url_frame, font=(font_name, font_size), bg = ENTRY_FIELD_BACKGROUND, fg = FOREGROUND) 
    url_entry.pack(side=tk.LEFT, padx=10)

    name_frame = tk.Frame(root, bg = DARK_BACKGROUND)  
    name_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    name_label = tk.Label(name_frame, text="Name:", font=(font_name, font_size,), bg = DARK_BACKGROUND, fg = FOREGROUND)
    name_label.pack(side=tk.LEFT, padx=3)

    name_entry = tk.Entry(name_frame, font=(font_name, font_size), bg = ENTRY_FIELD_BACKGROUND, fg = FOREGROUND) 
    name_entry.pack(side=tk.LEFT, padx=5)

    confirm_button = ctk.CTkButton(root, width=80, height=30, corner_radius=10, text="Create QR", text_color=FOREGROUND, command=lambda: qr_code(url_entry, name_entry), font=(font_name, font_size), fg_color=BUTTON_BACKGROUND, border_width=2, border_color=ENTRY_FIELD_BACKGROUND)  
    confirm_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    help_button = ctk.CTkButton(root, width=40, height=30, corner_radius=10, text="Help", text_color=FOREGROUND, command=show_help, font=(font_name, font_size), fg_color=BUTTON_BACKGROUND, border_width=2, border_color=ENTRY_FIELD_BACKGROUND)  
    help_button.place(relx=0.1, rely=0.9, anchor=tk.SW)

    quit_button = ctk.CTkButton(root, width=40, height=30, corner_radius=10, text="Quit", text_color=FOREGROUND, command=quit_application, font=(font_name, font_size), fg_color=BUTTON_BACKGROUND, border_width=2, border_color=ENTRY_FIELD_BACKGROUND)  
    quit_button.place(relx=0.9, rely=0.9, anchor=tk.SE)

    root.mainloop()
