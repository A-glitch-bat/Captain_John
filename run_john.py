# main.py
import tkinter as tk
from neon_button import create_neon_button

# Function to be executed when button is clicked
def on_button_click():
    print("Button clicked!")

# Main application setup
root = tk.Tk()
root.title("Neon Button Example")
root.configure(bg="black")

# Create a neon button and add it to the main window
neon_button = create_neon_button(root, text="Click Me", command=on_button_click)
neon_button.pack(pady=20)  # Pack or use .grid()/.place() as needed

# Run the application
root.mainloop()
