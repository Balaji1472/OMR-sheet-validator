import cv2
import tkinter as tk
import pytesseract
from PIL import Image,ImageTk
import os
import numpy as np
from tkinter import filedialog, messagebox
from tkinter import StringVar
from test import detect_marked_bubble_by_coordinates, label_marked_options_on_image, save_to_csv  # Import detection logic
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# ... (previous imports and global variables remain unchanged)

# Global variables
img_display = None
current_image_index = 0
image_files = []
processing_canceled = False
results = []  # To store results after processing
roll_number = ''  # To store detected roll number
score = 0  # To store the calculated score

# Predefined Answer Key for validation
answer_key = ['A', 'B', 'B', 'A', 'D', 'C', 'C', 'A', 'B', 'A',  # Example key for 10 questions
              'B', 'C', 'A', 'B', 'D', 'A', 'B', 'D', 'A','D']

# Function to refresh the entire GUI
def refresh_gui():
    global img_display, current_image_index, image_files, processing_canceled
    img_display = None
    current_image_index = 0
    image_files = []
    processing_canceled = False
    canvas.delete("all")
    result_text.set("Results will be displayed here.")
    score_text.set("")
    roll_number_text.set("")
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


def detect_name_section(image):
    # Define the dot coordinates for the name section
    name_dots = [
        (58, 89), (59, 102), (59, 113), (58, 126), (58, 138),
        (57, 151), (59, 163), (58, 176), (57, 187), (58, 199),
        (58, 211), (59, 224), (60, 235), (59, 248), (59, 260),
        (58, 273), (59, 284), (58, 297), (57, 309), (59, 322),
        (59, 333), (58, 346), (58, 357), (58, 369), (58, 383), (58, 393),
        (72, 89), (73, 101), (74, 114), (72, 125), (71, 139), (71, 151),
        (70, 161), (73, 176), (71, 187), (72, 199), (73, 210), (72, 223),
        (72, 236), (71, 249), (71, 258), (71, 273), (73, 285), (71, 297),
        (72, 309), (72, 320), (70, 333), (72, 344), (71, 359), (73, 371),
        (72, 382), (72, 391), (85, 89), (85, 102), (86, 113), (86, 125),
        (85, 138), (86, 150), (87, 162), (85, 174), (85, 187), (86, 199),
        (87, 210), (85, 223), (84, 235), (85, 248), (86, 261), (85, 273),
        (86, 285), (86, 298), (86, 310), (86, 320), (86, 334), (85, 347),
        (85, 358), (86, 370), (85, 382), (85, 396), (99, 91), (99, 102),
        (99, 114), (100, 127), (99, 139), (97, 149), (99, 163), (100, 174),
        (99, 188), (94, 200), (99, 210), (100, 224), (99, 236), (99, 247),
        (99, 259), (99, 271), (100, 286), (99, 297), (99, 309), (99, 321),
        (99, 333), (99, 345), (99, 357), (101, 370), (99, 383), (98, 394)
    ]
    
    # Create a bounding box around the dots
    min_x = min(dot[0] for dot in name_dots)
    max_x = max(dot[0] for dot in name_dots)
    min_y = min(dot[1] for dot in name_dots)
    max_y = max(dot[1] for dot in name_dots)
    
    # Extract the text within the bounding box
    roi = image[min_y:max_y+1, min_x:max_x+1]
    text = pytesseract.image_to_string(roi)
    
    return text.strip()

def process_omr_sheet():
    global results, roll_number, score

    if processing_canceled:
        result_text.set("Processing canceled.")
        return

    if not image_files:
        messagebox.showerror("Error", "No OMR sheets uploaded.")
        return

    current_image_path = image_files[current_image_index]
    image = cv2.imread(current_image_path)

    if image is None:
        messagebox.showerror("Error", f"Unable to load image at path '{current_image_path}'.")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 165, 255, cv2.THRESH_BINARY_INV)

    options_coordinates = [
       [(96, 468), (137, 466), (179, 467), (221, 467)],  # Question 1
        [(95, 480), (138, 479), (179, 480), (221, 480)],  # Question 2
        [(96, 492), (139, 491), (179, 494), (222, 492)],  # Question 3
        [(96,503),(138,503),(178,505),(220,504)],  
        [(95,518),(139,517),(178,517),(221,517)],
        [(97,528),(139,529),(178,527),(221,528)],
        [(96,541),(139,539),(178,538),(220,541)],
        [(95,552),(137,554),(178,553),(221,555)],
        [(95,565),(136,566),(180,563),(219,565)],
        [(95,578),(139,577),(179,577),(220,578)],
        [(95,590),(138,589),(179,590),(220,588)],
        [(97,603),(139,602),(178,603),(221,602)],
        [(95,614),(137,614),(179,616),(218,616)],
        [(97,626),(138,627),(180,627),(220,626)],
        [(96,638),(137,637),(178,638),(220,639)],
        [(95,651),(138,651),(178,649),(220,651)],
        [(95,664),(137,662),(181,663),(220,661)],
        [(96,675),(138,676),(179,673),(222,676)],
        [(97,687),(137,687),(178,688),(220,687)],
        [(96,701),(138,699),(178,699),(219,701)],
    ]


    roll_number_coordinates =  [
        [(328, 273), (328, 285), (329, 297), (328, 308), (329, 322), (329, 334), (329, 346), (329, 358), (329, 370), (329, 383)],
        [(345, 273), (346, 286), (344, 297), (345, 308), (346, 320), (345, 335), (346, 345), (346, 358), (346, 370), (345, 383)],
        [(361, 271), (360, 284), (361, 297), (361, 310), (361, 321), (361, 332), (362, 346), (361, 358), (362, 370), (361, 383)],
        [(377, 272), (378, 286), (377, 297), (380, 309), (377, 321), (376, 334), (377, 346), (378, 357), (378, 370), (380, 383)],
        [(392, 272), (393, 285), (395, 299), (396, 309), (395, 322), (395, 335), (394, 346), (392, 357), (394, 370), (394, 382)]
    ]

    option_texts = ['A', 'B', 'C', 'D']
    results = []

    # Detect options and roll number
    for question_idx, option_coords in enumerate(options_coordinates):
        marked_index = detect_marked_bubble_by_coordinates(binary_image, option_coords)
        label_marked_options_on_image(image, option_coords, option_texts, marked_index)
        marked_option = option_texts[marked_index] if marked_index >= 0 else "No answer"
        results.append((question_idx, marked_option))

    # Detect name
    name = detect_name_section(image)
    results.append(("Name", name))

    roll_number = ''
    for digit_coords in roll_number_coordinates:
        digit_index = detect_marked_bubble_by_coordinates(binary_image, digit_coords, mark_threshold=0.5)
        roll_number += str(digit_index) if digit_index >= 0 else 'X'

    # Validate score by comparing extracted options with the answer key
    score = 0

    for question_idx, (_, marked_option) in enumerate(results):
        if question_idx < len(answer_key):  # Ensure question_idx is within answer_key bounds
            if marked_option == answer_key[question_idx]:
                score += 1  # Increment score for correct answer
        else:
            messagebox.showwarning("Warning", f"Question {question_idx + 1} does not have a corresponding answer in the answer key.")

    # Display results in the UI
    result_text.set(f"Processing completed. Roll No: {roll_number}")
    score_text.set(f"Score: {score}/{len(answer_key)}")
    roll_number_text.set(f"Roll Number: {roll_number}")
    save_to_csv(name,results, roll_number)  # Save results to CSV

    processed_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(processed_image_rgb)
    img_display = ImageTk.PhotoImage(image=pil_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_display)

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

# Display Score
score_text = tk.StringVar()
score_label = tk.Label(result_frame, textvariable=score_text, font=("Arial", 12), fg="blue", bg="#ffffff")
score_label.pack()

# Display Roll Number
roll_number_text = tk.StringVar()
roll_label = tk.Label(result_frame, textvariable=roll_number_text, font=("Arial", 12), fg="blue", bg="#ffffff")
roll_label.pack()
#display name:



root.mainloop()
