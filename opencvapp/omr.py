import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import csv
from test import detect_marked_bubble_by_coordinates, label_marked_options_on_image, save_to_csv  # Import detection logic

# Global variables
img_display = None
current_image_index = 0
image_files = []
processing_canceled = False
results = [] 
roll_number = '' 
score = 0  

# Predefined Answer Key for validation
answer_key = ['A', 'B', 'B', 'A', 'D', 'C', 'C', 'A', 'B', 'A',  
              'B', 'C', 'A', 'B', 'D', 'A', 'B', 'D', 'A','D',
              'A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C','D',
              'A', 'B', 'A', 'B', 'B', 'C', 'B', 'C', 'C','D',
              'B', 'C', 'A', 'B', 'D', 'A', 'B', 'D', 'A','D',
              'A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C','D',
              'A', 'B', 'A', 'B', 'B', 'C', 'B', 'C', 'C','D',
              'B', 'C', 'A', 'B', 'D', 'A', 'B', 'D', 'A','D',
              'A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C','D']

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
        image = image.resize((400, 400))
        img_display = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {str(e)}")

# Function to process the OMR sheet
def process_omr_sheets():
    global results, roll_number, score

    if processing_canceled:
        result_text.set("Processing canceled.")
        return

    if not image_files:
        messagebox.showerror("Error", "No OMR sheets uploaded.")
        return

    # Initialize a list to store all results from multiple OMR sheets
    all_results = []

    # Loop over all OMR sheets
    for image_file in image_files:
        current_image_path = image_file
        image = cv2.imread(current_image_path)

        if image is None:
            messagebox.showerror("Error", f"Unable to load image at path '{current_image_path}'. Skipping this file.")
            continue

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 165, 255, cv2.THRESH_BINARY_INV)

        # Coordinates for options and roll number (same as before)
        options_coordinates = [
       [(96, 468), (137, 466), (179, 467), (221, 467)],
        [(95, 480), (138, 479), (179, 480), (221, 480)],
        [(96, 492), (139, 491), (179, 494), (222, 492)],
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
        [(97, 710),(138, 710),(181, 711),(221, 711)],
        [(96, 722),(137, 723),(179, 723),(221, 723)],
        [(97, 734),(137, 736),(180, 735),(222, 735)],
        [(95, 748),(137, 747),(180, 747),(222, 746)],
        [(97, 761),(138, 759),(180, 761),(220, 760)],
        [(96, 774),(138, 771),(179, 772),(220, 772)],
        [(98, 784),(137, 783),(180, 783),(221, 784)],
        [(96, 797),(138, 795),(180, 797),(223, 796)],
        [(97, 808),(137, 809),(177, 808),(221, 808)],
        [(97, 821),(137, 821),(180, 821),(221, 820)],
        [(311, 467),(355, 468),(397, 467),(436, 468)],
        [(312, 480),(352, 480),(393, 479),(436, 479)],
        [(312, 493),(353, 492),(396, 491),(435, 492)],
        [(312, 504),(354, 503),(394, 503),(437, 504)],
        [(312, 516),(353, 516),(395, 516),(436, 516)],
        [(310, 528),(353, 528),(394, 529),(435, 526)],
        [(313, 540),(352, 541),(396, 539),(436, 540)],
        [(311, 551),(353, 552),(394, 552),(435, 551)],
        [(311, 565),(354, 564),(393, 564),(435, 565)],
        [(311, 577),(354, 576),(395, 577),(436, 577)],
        [(311, 589),(353, 589),(394, 589),(435, 589)],
        [(312, 602),(353, 601),(394, 600),(435, 600)],
        [(311, 614),(353, 614),(396, 614),(436, 612)],
        [(311, 625),(353, 627),(397, 624),(436, 625)],
        [(313, 637),(353, 638),(395, 638),(436, 638)],
        [(312, 651),(355, 649),(394, 651),(436, 649)],
        [(311, 663),(353, 660),(393, 661),(436, 662)],
        [(312, 673),(353, 675),(395, 676),(438, 675)],
        [(311, 688),(353, 688),(394, 687),(434, 686)],
        [(311, 699),(352, 698),(395, 699),(435, 699)],
        [(310, 710),(353, 711),(394, 712),(436, 711)],
        [(311, 725),(351, 723),(393, 723),(436, 724)],
        [(311, 735),(351, 734),(394, 736),(434, 735)],
        [(309, 748),(351, 748),(392, 748),(435, 748)],
        [(311, 759),(351, 761),(394, 760),(436, 760)],
        [(312, 772),(351, 773),(394, 772),(436, 772)],
        [(310, 783),(352, 784),(394, 784),(436, 784)],
        [(312, 797),(353, 795),(394, 797),(435, 798)],
        [(312, 808),(352, 809),(394, 808),(435, 809)],
        [(309, 821),(351, 821),(394, 822),(436, 821)],
        [(528, 468),(569, 466),(609, 468),(654, 466)],
        [(527, 479),(570, 479),(611, 479),(652, 478)],
        [(524, 492),(570, 493),(611, 491),(653, 492)],
        [(527, 504),(569, 504),(612, 503),(652, 505)],
        [(527, 516),(571, 516),(610, 516),(652, 518)],
        [(528, 528),(570, 529),(610, 528),(653, 528)],
        [(527, 541),(568, 541),(610, 540),(653, 539)],
        [(527, 552),(569, 552),(612, 553),(652, 553)],
        [(526, 563),(570, 562),(611, 565),(653, 564)],
        [(526, 577),(567, 578),(609, 577),(651, 577)],
        [(527, 590),(570, 590),(612, 590),(651, 591)],
        [(528, 602),(568, 601),(611, 604),(652, 602)],
        [(526, 612),(569, 614),(609, 614),(651, 614)],
        [(526, 625),(569, 625),(610, 627),(650, 626)],
        [(527, 638),(571, 638),(610, 637),(651, 639)],
        [(526, 650),(567, 650),(610, 650),(650, 651)],
        [(527, 663),(567, 661),(610, 664),(652, 663)],
        [(528, 676),(569, 674),(612, 674),(653, 675)],
        [(527, 687),(567, 686),(611, 685),(650, 686)],
        [(526, 700),(569, 700),(610, 698),(653, 698)],
        [(526, 711),(569, 711),(610, 712),(653, 711)],
        [(526, 723),(568, 724),(610, 723),(652, 722)],
        [(527, 735),(568, 736),(608, 737),(651, 734)],
        [(527, 747),(568, 747),(610, 748),(651, 746)],
        [(526, 760),(567, 759),(610, 760),(652, 760)],
        [(530, 771),(566, 772),(610, 772),(650, 773)],
        [(527, 785),(569, 784),(611, 785),(652, 784)],
        [(525, 797),(569, 796),(610, 795),(651, 796)],
        [(526, 809),(568, 808),(610, 809),(650, 809)],
        [(526, 822),(568, 821),(610, 821),(652, 822)],   
    ]

        roll_number_coordinates = [
        [(328, 273), (328, 285), (329, 297), (328, 308), (329, 322), (329, 334), (329, 346), (329, 358), (329, 370), (329, 383)],
        [(345, 273), (346, 286), (344, 297), (345, 308), (346, 320), (345, 335), (346, 345), (346, 358), (346, 370), (345, 383)],
        [(361, 271), (360, 284), (361, 297), (361, 310), (361, 321), (361, 332), (362, 346), (361, 358), (362, 370), (361, 383)],
        [(377, 272), (378, 286), (377, 297), (380, 309), (377, 321), (376, 334), (377, 346), (378, 357), (378, 370), (380, 383)],
        [(392, 272), (393, 285), (395, 299), (396, 309), (395, 322), (395, 335), (394, 346), (392, 357), (394, 370), (394, 382)]
    ]

        option_texts = ['A', 'B', 'C', 'D']
        results = []

        # Detect options and roll number for the current sheet
        for question_idx, option_coords in enumerate(options_coordinates):
            marked_index = detect_marked_bubble_by_coordinates(binary_image, option_coords)
            label_marked_options_on_image(image, option_coords, option_texts, marked_index)
            marked_option = option_texts[marked_index] if marked_index >= 0 else "No answer"
            results.append((question_idx, marked_option))

        roll_number = ''
        for digit_coords in roll_number_coordinates:
            digit_index = detect_marked_bubble_by_coordinates(binary_image, digit_coords, mark_threshold=0.5)
            roll_number += str(digit_index) if digit_index >= 0 else 'X'

        # Validate score by comparing extracted options with the answer key
        score = 0
        for question_idx, (_, marked_option) in enumerate(results):
            if question_idx < len(answer_key): 
                if marked_option == answer_key[question_idx]:
                    score += 1
            else:
                messagebox.showwarning("Warning", f"Question {question_idx + 1} does not have a corresponding answer in the answer key.")

        # Append results for the current sheet (roll number and answers) to the all_results list
        all_results.append([roll_number] + [marked_option for _, marked_option in results])

        # Update the canvas with processed image (showing detected answers)
        processed_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(processed_image_rgb)
        img_display = ImageTk.PhotoImage(image=pil_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)

    # Save all results to the CSV
    save_multiple_to_csv(all_results)

    # Display results for the last processed sheet in the UI
    result_text.set(f"Processing completed for all sheets.")
    score_text.set(f"Last Sheet Score: {score}/{len(answer_key)}")
    roll_number_text.set(f"Last Processed Roll Number: {roll_number}")


def save_multiple_to_csv(all_results):
    # Define the CSV file path
    csv_file_path = "omr_results.csv"

    # Open the CSV file in append mode
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is empty
        if file.tell() == 0:
            header = ['Roll Number'] + [f'Q{q+1}' for q in range(len(all_results[0]) - 1)]
            writer.writerow(header)

        # Write all the results (appends rows to the CSV)
        writer.writerows(all_results)

# Function to move to the next OMR sheet
def next_omr_sheet():
    global current_image_index
    if not image_files:
        messagebox.showerror("Error", "No OMR sheets uploaded.")
        return

    if current_image_index < len(image_files) - 1:
        current_image_index += 1
        load_image(image_files[current_image_index])
    else:
        messagebox.showinfo("Info", "This is the last image.")

# Function to move to the previous OMR sheet
def previous_omr_sheet():
    global current_image_index
    if not image_files:
        messagebox.showerror("Error", "No OMR sheets uploaded.")
        return

    if current_image_index > 0:
        current_image_index -= 1
        load_image(image_files[current_image_index])
    else:
        messagebox.showinfo("Info", "This is the first image.")

# GUI setup
root = tk.Tk()
root.title("OMR Validator")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Control panel
control_frame = tk.Frame(root)
control_frame.pack()

upload_button = tk.Button(control_frame, text="Upload OMR Folder", command=upload_omr_folder)
upload_button.grid(row=0, column=0)

process_button = tk.Button(control_frame, text="Process OMR Sheet", command=process_omr_sheets)
process_button.grid(row=0, column=1)

prev_button = tk.Button(control_frame, text="Previous", command=previous_omr_sheet)
prev_button.grid(row=0, column=2)

next_button = tk.Button(control_frame, text="Next", command=next_omr_sheet)
next_button.grid(row=0, column=3)

refresh_button = tk.Button(control_frame, text="Refresh", command=refresh_gui)
refresh_button.grid(row=0, column=4)

# Labels for displaying results
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.pack()

score_text = tk.StringVar()
score_label = tk.Label(root, textvariable=score_text)
score_label.pack()

roll_number_text = tk.StringVar()
roll_number_label = tk.Label(root, textvariable=roll_number_text)
roll_number_label.pack()

# Start the GUI event loop
root.mainloop()
