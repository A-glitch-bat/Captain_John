import tkinter as tk
import subprocess
import os

# Function to open VS Code with the specified folder
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

    # Clear the text widget and display the output
    output_text.delete(1.0, tk.END)  # Clear previous text
    if stdout:
        output_text.insert(tk.END, f"Output:\n{stdout}\n")
    if stderr:
        output_text.insert(tk.END, f"Errors:\n{stderr}\n")

# Function to print a line of text in the text widget
def print_text():
    output_text.insert(tk.END, "This is a simple line of text.\n")


# Create the main window
root = tk.Tk()
root.title("John")

# Create a button that opens VS Code
button_vscode = tk.Button(root, text="Open VS Code", command=open_vscode)
button_vscode.pack(pady=5)

# Create a button that prints a line of text
button_print = tk.Button(root, text="Print Text", command=print_text)
button_print.pack(pady=5)

# Create a text widget to display the terminal output
output_text = tk.Text(root, wrap='word', height=15, width=60)
output_text.pack(padx=10, pady=10)

# Run the application
root.mainloop()
