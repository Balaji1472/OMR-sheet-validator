import cv2
import numpy as np
from tkinter import Tk, Canvas
from PIL import Image, ImageTk
import csv

def detect_marked_bubble_by_coordinates(binary_image, coordinates, mark_threshold=0.5):
    max_fill_ratio = 0
    marked_index = -1  # No bubble is marked initially

    for idx, (x, y) in enumerate(coordinates):
        bubble_roi = binary_image[y - 5:y + 5, x - 5:x + 5]
        total_pixels = bubble_roi.size
        black_pixels = cv2.countNonZero(bubble_roi)
        fill_ratio = black_pixels / float(total_pixels)

        if fill_ratio > max_fill_ratio and fill_ratio > mark_threshold:
            max_fill_ratio = fill_ratio
            marked_index = idx

    return marked_index

def label_marked_options_on_image(image, coordinates, option_texts, marked_index):
    if marked_index >= 0:
        x, y = coordinates[marked_index]
        cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 255, 0), 2)
        option = option_texts[marked_index]
        cv2.putText(image, option, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

def save_to_csv(results, roll_number, filename="omr_results.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Roll Number", roll_number])  # Roll number at the top
        writer.writerow(["Question", "Marked Option"])  # Header row for questions
        for question, option in results:
            writer.writerow([f"Question {question + 1}", option])

def main():
    root = Tk()
    root.title("OMR Sheet with Marked Bubbles")

    image_path = "fomr.jpg"
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at path '{image_path}'. Check the file path.")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 165, 255, cv2.THRESH_BINARY_INV)

    areas = {
        "Questions": (63, 452, 238, 832),
    }

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

    roll_number_coordinates = [
        [(328, 273), (328, 285), (329, 297), (328, 308), (329, 322), (329, 334), (329, 346), (329, 358), (329, 370), (329, 383)],
        [(345, 273), (346, 286), (344, 297), (345, 308), (346, 320), (345, 335), (346, 345), (346, 358), (346, 370), (345, 383)],
        [(361, 271), (360, 284), (361, 297), (361, 310), (361, 321), (361, 332), (362, 346), (361, 358), (362, 370), (361, 383)],
        [(377, 272), (378, 286), (377, 297), (380, 309), (377, 321), (376, 334), (377, 346), (378, 357), (378, 370), (380, 383)],
        [(392, 272), (393, 285), (395, 299), (396, 309), (395, 322), (395, 335), (394, 346), (392, 357), (394, 370), (394, 382)]
    ]

    option_texts = ['A', 'B', 'C', 'D']

    results = []

    output_image = image.copy()

    for question_idx, option_coords in enumerate(options_coordinates):
        marked_index = detect_marked_bubble_by_coordinates(binary_image, option_coords)
        label_marked_options_on_image(output_image, option_coords, option_texts, marked_index)
        marked_option = option_texts[marked_index] if marked_index >= 0 else "No answer"
        results.append((question_idx, marked_option))

    roll_number = ''
    for digit_coords in roll_number_coordinates:
        digit_index = detect_marked_bubble_by_coordinates(binary_image, digit_coords, mark_threshold=0.5)
        roll_number += str(digit_index) if digit_index >= 0 else 'X'  # Use 'X' if no answer is marked

    print(f"Detected Roll Number: {roll_number}")

    save_to_csv(results, roll_number, filename="omr_results.csv")

    resize_factor = 0.5
    resized_image = cv2.resize(output_image, None, fx=resize_factor, fy=resize_factor)
    resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(resized_image_rgb)
    tk_image = ImageTk.PhotoImage(image=pil_image)

    canvas = Canvas(root, width=pil_image.width, height=pil_image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=tk_image)

    root.mainloop()

if __name__ == "__main__":
    main()
