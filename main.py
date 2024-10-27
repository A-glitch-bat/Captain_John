#--------------------------------

# Imports
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import subprocess
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

def print_text():
    output_text.insert(tk.END, "This is a simple line of text.\n")
#--------------------------------

# Define app
root = tk.Tk()
root.title("John")
root.configure(bg='black')
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

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg='black')
button_frame.grid(row=0, column=0, pady=20)

button_vscode = tk.Button(root, text="Open VS Code", command=open_vscode,
                          bg='black', fg='lime', activebackground='black', activeforeground='lime',
                          highlightbackground='lime', highlightthickness=2)
button_vscode.grid(row=0, column=0, padx=10)

# Create a canvas to act as a custom button
rounded_button = tk.Canvas(root, width=button_width, height=button_height, bg='black', highlightthickness=0)
rounded_button.create_image(0, 0, anchor="nw", image=default_image, tags="button_image")
rounded_button.create_text(button_width // 2, button_height // 2, text="Click Me", 
                           fill="white", font=("Arial", 16, "bold"), tags="button_text")
rounded_button.grid(row=0, column=1, padx=10, pady=20)

# Bind mouse events to the canvas itself to simulate button press and release
rounded_button.bind("<ButtonPress-1>", lambda event: on_button_press(event, rounded_button, pressed_image))
rounded_button.bind("<ButtonRelease-1>", lambda event: on_button_release(event, rounded_button, default_image, print_text))

# Create a text widget to display output
output_text = tk.Text(root, wrap='word', height=15, width=60, bg='black', fg='lime',
                      insertbackground='lime', highlightbackground='lime', highlightthickness=2)
output_text.grid(row=1, column=0, padx=10, pady=10)
#--------------------------------

# Wake John up
root.mainloop()
#--------------------------------
