import tkinter as tk
from tkinter import messagebox
import os
import sys
import pyqrcode as qr
import customtkinter as ctk


def get_script_directory():
    return os.path.dirname(sys.argv[0])

script_directory = get_script_directory()

# Colours

DARK_BACKGROUND = '#1E2E3E'
BUTTON_BACKGROUND = '#0F1F3F'
FOREGROUND = '#EFEFFF'
ENTRY_FIELD_BACKGROUND = '#3C4D5E'

# Font
font_name = 'Verdana'
font_size = 12

#Functions
def save_qr(name, png_folder):

    '''
    saves qr as png
    
    param: name -> if empty, save as QRx where x is the most recent value of a blank name in the save folder
                                else save as the given name in name entry field
    
    '''

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


def qr_code(url_entry, name_entry):

    '''
    creates qr code, saves and opens png

    param: url_entry -> take in a user input to define the link address
                 name_entry -> take in a user input to define the name of the qr code to be created respectively
    '''

    url_str = url_entry.get()

    url = error_correct(url_str)
    
    name = name_entry.get()

    subfolder_name = 'PNGs'
    png_folder = os.path.join(script_directory, subfolder_name)
    os.makedirs(png_folder, exist_ok=True)

    png_name = save_qr(name, png_folder)

    url_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    png_path = os.path.abspath(os.path.join(png_folder, f'{png_name}.png'))
    url.png(png_path, scale=5)

    os.system(f'start "" "{png_path}"')

    
def quit_application():
    confirm_quit = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if confirm_quit:
        root.destroy()


def show_help():
    help_message = ("Enter your URL and a Name for the QR code into the entry boxes."
                     + '\n' + "Selected a value on the slider for error correction and redundancy."
                       + '\n' + "Finally, press enter to create your QR code." + '\n''\n' + 'Note*'
                         +'\n''\n'+ "Higher redundancy leads to bigger QR codes, which due to increased error protection, may require more space and hold less data, leading to slower scanning and potential compatibility issues with some scanners."
                           + '\n''\n' "However, lower levels of redundacy may make the QR codes more susceptible to errors or damage, which can lead to difficulties in scanning and retrieving accurate data.")
    
    messagebox.showinfo("Help", help_message)


def map_to_labels(value):

    '''
    returns error correction level value for display
    '''
    
    levels = ["0", "L = 7%", "M = 15%", "Q = 25%", "H = 30%"]
    index = int(value)
    return levels[index]


def slider_event(value):
    
    '''
    maps slider value to error correction level value to display
    '''

    slider_label.configure(text=map_to_labels(value))
    return value


def error_correct(url_str):

    '''
    maps slider value to error correction value when creating QR code
    '''

    error_level = int(slider.get())
    error_levels = [1, 2, 3, 4]
    correction_level = ["L", "M", "Q", "H"]

    if error_level in error_levels:
        print(error_level)
        err = correction_level[int(error_level) - 1]
        print(err)
        url = qr.create(url_str, error = err)

    else:
        url = qr.create(url_str)
        print("error not used")
 
    return url


# Main
if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("400x300")
    root.resizable(False, False)
    root.title("QR Code Generator")
    root.iconbitmap("myIcon.ico")
    root.configure(bg=DARK_BACKGROUND)

    slider = ctk.CTkSlider(master=root,
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
                                 command=slider_event)
    slider.set(1)
    slider.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    slider_label = ctk.CTkLabel(master=root, text='', font=(font_name, font_size))
    slider_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    url_frame = tk.Frame(root, bg = DARK_BACKGROUND)  
    url_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    url_label = tk.Label(url_frame, text="URL:", font=(font_name, font_size), bg = DARK_BACKGROUND, fg = FOREGROUND,)  # Dark background, white text
    url_label.pack(side=tk.LEFT, padx=10)

    url_entry = tk.Entry(url_frame, font=(font_name, font_size), bg = ENTRY_FIELD_BACKGROUND, fg = FOREGROUND) 
    url_entry.pack(side=tk.LEFT, padx=10)

    name_frame = tk.Frame(root, bg = DARK_BACKGROUND)  
    name_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    name_label = tk.Label(name_frame, text="Name:", font=(font_name, font_size,), bg = DARK_BACKGROUND, fg = FOREGROUND)  # Dark background, white text
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