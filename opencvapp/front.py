import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Global variables
img_display = None
current_image_index = 0
image_files = []
processing_canceled = False

# Function to refresh the entire GUI
def refresh_gui():
    global img_display, current_image_index, image_files, processing_canceled
    img_display = None
    current_image_index = 0
    image_files = []
    processing_canceled = False
    canvas.delete("all")
    result_text.set("Results will be displayed here.")
    messagebox.showinfo("Info", "The interface has been refreshed.")

# Function to upload a folder with OMR sheets
def upload_omr_folder():
    global image_files, current_image_index
    folder_path = filedialog.askdirectory()
    if folder_path:
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                       if f.endswith(('.jpg', '.png', '.jpeg', '.bmp'))]
        if not image_files:
            messagebox.showerror("Error", "No valid image files found in the folder.")
            return
        current_image_index = 0
        load_image(image_files[current_image_index])

# Function to load and display the current OMR image
def load_image(file_path):
    global img_display
    try:
        image = Image.open(file_path)
        image = image.resize((400, 400))  # Resize the image to fit in canvas
        img_display = ImageTk.PhotoImage(image)
        canvas.delete("all")  # Clear previous image
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {str(e)}")

# Function to process the OMR sheet
def process_omr_sheet():
    if processing_canceled:
        result_text.set("Processing canceled.")
        return
    result_text.set(f"Processing completed. Marks: 90, Name: John Doe, Roll No: 12345.")

# Function to move to the next image
def next_image():
    global current_image_index
    if not image_files:
        messagebox.showerror("Error", "No OMR sheets uploaded.")
        return
    if current_image_index < len(image_files) - 1:
        current_image_index += 1
        load_image(image_files[current_image_index])
    else:
        messagebox.showinfo("Info", "This is the last image.")

# Function to move to the previous image
def previous_image():
    global current_image_index
    if not image_files:
        messagebox.showerror("Error", "No OMR sheets uploaded.")
        return
    if current_image_index > 0:
        current_image_index -= 1
        load_image(image_files[current_image_index])
    else:
        messagebox.showinfo("Info", "This is the first image.")

# Function to cancel the process
def cancel_process():
    global processing_canceled
    processing_canceled = True
    result_text.set("Operation canceled by the user.")

# Initialize main window
root = tk.Tk()
root.title("OMR Sheet Validator")
root.geometry("650x750")  # Adjusted window size for refresh option

# Header Section
header = tk.Label(root, text="OMR Sheet Validator", font=("Arial", 20), bg="#3498db", fg="white")
header.pack(pady=10)

# File Upload Section
upload_frame = tk.Frame(root, bg="#ffffff")
upload_frame.pack(pady=10)

upload_button = tk.Button(upload_frame, text="Upload OMR Folder", command=upload_omr_folder, bg="#27ae60", fg="white")
upload_button.pack(side=tk.LEFT, padx=5)

# OMR Image Display Section
canvas_frame = tk.Frame(root, bg="#ffffff")
canvas_frame.pack()

canvas = tk.Canvas(canvas_frame, width=400, height=400, bg="lightgray")
canvas.pack()

# Navigation Arrows (Previous, Next)
nav_frame = tk.Frame(root, bg="#ffffff")
nav_frame.pack(pady=10)

prev_button = tk.Button(nav_frame, text="← Previous", command=previous_image, bg="#3498db", fg="white")
prev_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(nav_frame, text="Next →", command=next_image, bg="#3498db", fg="white")
next_button.pack(side=tk.LEFT, padx=10)

# Process and Cancel Buttons
button_frame = tk.Frame(root, bg="#ffffff")
button_frame.pack(pady=10)

process_button = tk.Button(button_frame, text="Process OMR Sheet", command=process_omr_sheet, bg="#27ae60", fg="white")
process_button.pack(side=tk.LEFT, padx=5)

cancel_button = tk.Button(button_frame, text="Cancel Process", command=cancel_process, bg="#e74c3c", fg="white")
cancel_button.pack(side=tk.LEFT, padx=5)

# Refresh Button
refresh_button = tk.Button(button_frame, text="Refresh", command=refresh_gui, bg="#3498db", fg="white")
refresh_button.pack(side=tk.LEFT, padx=5)

# Results Section
result_frame = tk.Frame(root, bg="#ffffff")
result_frame.pack(pady=10)

result_text = tk.StringVar()
result_text.set("Results will be displayed here.")
result_label = tk.Label(result_frame, textvariable=result_text, font=("Arial", 12), fg="green", bg="#ffffff")
result_label.pack()

# Start the application
root.mainloop()
