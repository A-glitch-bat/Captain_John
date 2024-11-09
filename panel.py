#--------------------------------

# Imports
import tkinter as tk
import psutil
#--------------------------------

# Semi-transparent panel for info display
def info_panel():
    panel = tk.Toplevel()
    panel.geometry("300x300+50+450") # Size and position
    panel.title("INFO")
    panel.configure(bg="#1a1a1a")  # Set background color for the cyberpunk theme
    panel.attributes("-alpha", 0.75)  # Set transparency
    #--------------------------------
    panel.overrideredirect(True)  # Remove the default title bar
    #--------------------------------

    # Outer frame to act as an outline
    outline_frame = tk.Frame(panel, bg="hotpink")  # Border color
    outline_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Adjust padding for border thickness

    # Inner frame for the actual content
    content_frame = tk.Frame(outline_frame, bg="#1a1a1a")  # Main content background color
    content_frame.pack(fill="both", expand=True)

    # Custom title bar within the inner frame
    title_bar = tk.Frame(content_frame, bg="#1a1a1a", relief="raised", bd=0)
    title_bar.pack(fill="x")

    title_label = tk.Label(title_bar, text="System Info", bg="#1a1a1a", fg="hotpink", font=("Arial", 10, "bold"))
    title_label.pack(side="left", padx=5)

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
    # ---------------------------------------------

    # Canvas for CPU and RAM usage
    cpu_canvas = tk.Canvas(panel, width=100, height=100, bg="#1a1a1a", highlightthickness=0)
    cpu_canvas.pack(pady=10)

    ram_canvas = tk.Canvas(panel, width=100, height=100, bg="#1a1a1a", highlightthickness=0)
    ram_canvas.pack(pady=10)

    # Labels for CPU and RAM usage
    cpu_label = tk.Label(cpu_canvas, text="CPU: --%", fg="magenta", bg="#1a1a1a", font=("Arial", 10, "bold"))
    cpu_label.place(relx=0.5, rely=0.5, anchor="center")

    ram_label = tk.Label(ram_canvas, text="RAM: --%", fg="magenta", bg="#1a1a1a", font=("Arial", 10, "bold"))
    ram_label.place(relx=0.5, rely=0.5, anchor="center")

    # Initialise
    cpu_label.config(text=f"CPU: {psutil.cpu_percent(interval=0)}%")  # Immediate CPU reading
    ram_label.config(text=f"RAM: {psutil.virtual_memory().percent}%")  # Immediate RAM reading

    cpu_canvas.create_arc(10, 10, 90, 90, start=90, extent=(psutil.cpu_percent(interval=0) * 3.6),
                          outline="hotpink", width=8, style="arc", tags="arc")
    ram_canvas.create_arc(10, 10, 90, 90, start=90, extent=(psutil.virtual_memory().percent * 3.6),
                          outline="hotpink", width=8, style="arc", tags="arc")
    #--------------------------------
    def update_gauges():
        # Get CPU and RAM usage
        cpu_percent = psutil.cpu_percent(interval=1)  # Smooth updates
        ram_percent = psutil.virtual_memory().percent
        cpu_label.config(text=f"CPU: {cpu_percent}%")
        ram_label.config(text=f"RAM: {ram_percent}%")

        # CPU arc
        cpu_canvas.delete("arc")  # Remove the previous arc
        cpu_canvas.create_arc(10, 10, 90, 90, start=90, extent=(cpu_percent * 3.6),
                              outline="hotpink", width=8, style="arc", tags="arc")

        # RAM arc
        ram_canvas.delete("arc")  # Remove the previous arc
        ram_canvas.create_arc(10, 10, 90, 90, start=90, extent=(ram_percent * 3.6),
                              outline="hotpink", width=8, style="arc", tags="arc")

        panel.after(1000, update_gauges)
    #--------------------------------

    # Update every second
    panel.after(1000, update_gauges)
#--------------------------------
