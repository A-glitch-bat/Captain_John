# neon_button.py
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def create_neon_glow(radius, button_width, button_height, glow_color):
    # Create an image with transparency
    glow_image = Image.new("RGBA", (button_width + radius*2, button_height + radius*2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_image)
    
    # Draw a soft-edged glow around a rectangle
    for i in range(radius, 0, -1):
        alpha = int(255 * (i / radius))
        draw.rectangle(
            (radius - i, radius - i, button_width + i, button_height + i),
            outline=glow_color,
            width=1
        )
    
    return ImageTk.PhotoImage(glow_image)

def create_neon_button(root, text, command, button_width=100, button_height=40, glow_radius=20, glow_color="#00FF00"):
    # Create a canvas to hold the glow background
    canvas = tk.Canvas(root, width=button_width + glow_radius*2, height=button_height + glow_radius*2, bg="black", highlightthickness=0)
    
    # Generate the glow effect and add it to the canvas
    neon_glow = create_neon_glow(glow_radius, button_width, button_height, glow_color)
    canvas.create_image(0, 0, image=neon_glow, anchor="nw")
    
    # Place a standard tk.Button over the glow effect
    button = tk.Button(root, text=text, command=command, bg="lime", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2")
    canvas.create_window(glow_radius, glow_radius, anchor="nw", window=button)
    
    # Return the canvas containing the neon glow and button
    return canvas
