#--------------------------------

# Imports
import tkinter as tk
#--------------------------------

# Semi-transparent panel for info display
def info_panel():
    panel = tk.Toplevel()
    panel.geometry("250x150+550+450") # Size and position
    panel.title("INFO")
    panel.configure(bg="#1a1a1a")  # Set background color for the cyberpunk theme
    panel.attributes("-alpha", 0.75)  # Set transparency
    #--------------------------------
    panel.overrideredirect(True)  # Remove the default title bar
    #--------------------------------

    # Create a custom title bar
    title_bar = tk.Frame(panel, bg="#1a1a1a", relief="raised", bd=0)
    title_bar.pack(fill="x")

    # Title bar text
    title_label = tk.Label(title_bar, text="Extra Panel", bg="#1a1a1a", fg="hotpink", font=("Arial", 10, "bold"))
    title_label.pack(side="left", padx=5)

    # Close button on custom title bar
    close_button = tk.Button(title_bar, text="X", bg="#1a1a1a", fg="red", font=("Arial", 10, "bold"), 
                             command=panel.destroy, relief="flat", cursor="hand2")
    close_button.pack(side="right", padx=5)
    #--------------------------------

    # Allow dragging the custom title bar
    def start_move(event):
        panel.x = event.x
        panel.y = event.y

    def stop_move(event):
        panel.x = None
        panel.y = None

    def on_motion(event):
        delta_x = event.x - panel.x
        delta_y = event.y - panel.y
        new_x = panel.winfo_x() + delta_x
        new_y = panel.winfo_y() + delta_y
        panel.geometry(f"+{new_x}+{new_y}")
    #--------------------------------

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)
    title_bar.bind("<B1-Motion>", on_motion)
#--------------------------------
