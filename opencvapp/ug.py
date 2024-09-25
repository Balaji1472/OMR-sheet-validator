import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import PhotoImage

class OMRValidatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OMR Sheet Validator")
        self.root.geometry("600x400")

        # Load background image
        self.bg_image = PhotoImage(file="background.png")  # Replace with your image path
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create frames with a transparent background
        self.upload_frame = tk.Frame(self.root, bg="#ffffff", bd=5)
        self.upload_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.process_frame = tk.Frame(self.root, bg="#ffffff", bd=5)
        self.process_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.cancel_frame = tk.Frame(self.root, bg="#ffffff", bd=5)
        self.cancel_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Create colorful buttons and entry fields
        self.answer_key_label = tk.Label(self.upload_frame, text="Upload Answer Key:", bg="#ffffff", fg="#333333")
        self.answer_key_label.grid(row=0, column=0, padx=5, pady=5)

        self.answer_key_entry = tk.Entry(self.upload_frame, width=50)
        self.answer_key_entry.grid(row=0, column=1, padx=5, pady=5)

        self.answer_key_button = tk.Button(self.upload_frame, text="Browse", command=self.upload_answer_key, bg="#4CAF50", fg="white")
        self.answer_key_button.grid(row=0, column=2, padx=5, pady=5)

        self.folder_label = tk.Label(self.upload_frame, text="Upload Folder:", bg="#ffffff", fg="#333333")
        self.folder_label.grid(row=1, column=0, padx=5, pady=5)

        self.folder_entry = tk.Entry(self.upload_frame, width=50)
        self.folder_entry.grid(row=1, column=1, padx=5, pady=5)

        self.folder_button = tk.Button(self.upload_frame, text="Browse", command=self.upload_folder, bg="#4CAF50", fg="white")
        self.folder_button.grid(row=1, column=2, padx=5, pady=5)

        # Process button
        self.process_button = tk.Button(self.process_frame, text="Process", command=self.process_omr, bg="#2196F3", fg="white", width=20)
        self.process_button.pack(pady=10)

        # Cancel button
        self.cancel_button = tk.Button(self.cancel_frame, text="Cancel", command=self.cancel, bg="#f44336", fg="white", width=20)
        self.cancel_button.pack(pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Idle", bg="#ffffff", fg="#000000")
        self.status_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def upload_answer_key(self):
        file_path = filedialog.askopenfilename(title="Select Answer Key File", filetypes=[("PDF files", "*.pdf")])
        self.answer_key_entry.delete(0, tk.END)
        self.answer_key_entry.insert(0, file_path)

    def upload_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder for Bulk Processing")
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, folder_path)

    def process_omr(self):
        # Add your OMR processing logic here
        self.status_label.config(text="Status: Processing...")
        self.progress_bar.start()
        # Simulate processing time
        self.root.after(5000, self.process_complete)

    def cancel(self):
        # Add your cancel logic here
        self.status_label.config(text="Status: Cancelled")
        self.progress_bar.stop()

    def process_complete(self):
        self.status_label.config(text="Status: Complete")
        self.progress_bar.stop()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = OMRValidatorGUI()
    gui.run()
