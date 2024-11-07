#--------------------------------

# Imports
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import subprocess
from neon_button import create_neon_button
from panel import info_panel
#--------------------------------

# Functions
def open_vscode():
    folder_path = "C:\\John"
    process = subprocess.Popen(
        ["code", folder_path], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True, 
        shell=True, 
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    stdout, stderr = process.communicate()

    # Clear the text widget and display output
    #output_text.delete(1.0, tk.END)  # (clearing disabled)
    if stdout:
        output_text.insert(tk.END, f"Output:\n{stdout}\n")
    if stderr:
        output_text.insert(tk.END, f"Errors:\n{stderr}\n")

def create_rounded_button(width, height, radius, border_thickness, color, outer_border_color, inner_border_color):
    # Create a rounded rectangle image with transparency
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw the outer border (3D effect)
    draw.rounded_rectangle(
        (0, 0, width, height),
        radius,
        fill=None,
        outline=outer_border_color,
        width=border_thickness
    )

    # Draw the inner black border
    inner_offset = border_thickness
    draw.rounded_rectangle(
        (inner_offset, inner_offset, width - inner_offset, height - inner_offset),
        radius - border_thickness,
        fill=None,
        outline=inner_border_color,
        width=border_thickness
    )

    # Fill the main button area with the specified color
    main_offset = 2 * border_thickness
    draw.rounded_rectangle(
        (main_offset, main_offset, width - main_offset, height - main_offset),
        radius - 2 * border_thickness,
        fill=color
    )

    return ImageTk.PhotoImage(image)

def on_button_press(event, button, pressed_image):
    # Change the button appearance when pressed
    button.config(image=pressed_image)
    button.image = pressed_image

def on_button_release(event, button, default_image, command):
    # Restore the button appearance after release
    button.config(image=default_image)
    button.image = default_image
    # Execute the command
    command()
#--------------------------------

# Define app
root = tk.Tk()
root.configure(bg="black") #250x150
root.geometry("550x400+200+150")  # Custom position
root.overrideredirect(True)  # Remove the default title bar

# Remove default title bar and create a new grid setup
title_bar = tk.Frame(root, bg="black", relief="raised", bd=0)
title_bar.grid(row=0, column=0, columnspan=3, sticky="we")

# Title label on the custom title bar
title_label = tk.Label(title_bar, text="Captain John", bg="black", fg="cyan", font=("Arial", 10, "bold"))
title_label.pack(side="left", padx=5)

# Close button on the custom title bar
close_button = tk.Button(title_bar, text="X", bg="black", fg="red", font=("Arial", 10, "bold"),
                         command=root.destroy, relief="flat", cursor="hand2")
close_button.pack(side="right", padx=5)

# Allow dragging the custom title bar
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_motion(event):
    delta_x = event.x - root.x
    delta_y = event.y - root.y
    new_x = root.winfo_x() + delta_x
    new_y = root.winfo_y() + delta_y
    root.geometry(f"+{new_x}+{new_y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", on_motion)
#--------------------------------

# Define elements
button_width, button_height = 75, 50
button_radius = 10
button_border_thickness = 2
button_color = "#00FF00"  # Lime green color
outer_border_color = "#00CC00"  # Slightly darker lime green
inner_border_color = "black"  # Inner border color

# Create button images for default and pressed states
default_image = create_rounded_button(
    button_width, button_height, button_radius,
    button_border_thickness, button_color,
    outer_border_color, inner_border_color
)
pressed_image = create_rounded_button(
    button_width, button_height, button_radius,
    button_border_thickness, "#00CC00",  # Darker green when pressed
    outer_border_color, inner_border_color
)
#--------------------------------
# Button frame
button_frame = tk.Frame(root, bg="black")
button_frame.grid(row=1, column=0, columnspan=3, pady=20)
#--------------------------------
button_vscode = tk.Button(root, text="Open VS Code", command=open_vscode,
                          bg='black', fg='lime', activebackground='black', activeforeground='lime',
                          highlightbackground='lime', highlightthickness=2)
button_vscode.grid(row=1, column=0, padx=10, pady=5)
#--------------------------------
def on_button_click(output_widget):
    output_widget.insert(tk.END, "Button clicked!\n")
neon_button = create_neon_button(root, text="Click Me", command=lambda: on_button_click(output_text))
neon_button.grid(row=1, column=1, padx=10, pady=5)
#--------------------------------
open_panel_button = tk.Button(button_frame, text="Open Extra Panel", command=info_panel,
                              bg="black", fg="lime", font=("Arial", 12, "bold"), cursor="hand2", relief="flat")
open_panel_button.grid(row=1, column=2, padx=10, pady=5)
#--------------------------------

# Create a text widget to display output
output_text = tk.Text(root, wrap='word', height=15, width=60, bg='black', fg='lime',
                      insertbackground='lime', highlightbackground='lime', highlightthickness=2)
output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
#--------------------------------

# Wake John up
root.mainloop()
#--------------------------------
