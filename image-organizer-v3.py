import os
import shutil
from datetime import datetime
from typing import List, Tuple
from PIL import Image, ExifTags, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog, ttk
from collections import defaultdict

def search_images(directory: str) -> List[str]:
    """
    Search for image files in the specified directory.

    :param directory: Directory to search for images.
    :return: List of image file paths.
    """
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    images = []
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                images.append(os.path.join(subdir, file))
    print(f"Total images found: {len(images)}")
    return images

def get_image_metadata(image_path: str) -> Tuple[datetime.date, str]:
    """
    Extract the date the image was taken from EXIF data, or use the file's last modified date if EXIF data is not available.

    :param image_path: Path to the image file.
    :return: A tuple containing the date the image was taken and the original file name.
    """
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                date_time_original_tag = next(
                    (ExifTags.TAGS[k] for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'DateTimeOriginal'),
                    None)
                if date_time_original_tag and date_time_original_tag in exif_data:
                    date_taken = exif_data[date_time_original_tag]
                    date_str = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').date()
                    return date_str, os.path.basename(image_path)
            # If no EXIF or date wasn't found, default to the file's last modified time
            last_modified_time = os.path.getmtime(image_path)
            date_str = datetime.fromtimestamp(last_modified_time).date()
            return date_str, os.path.basename(image_path)
    except (UnidentifiedImageError, Exception):
        return None, os.path.basename(image_path)

def copy_images_by_date(images: List[str], output_directory: str, progress_callback: callable) -> None:
    """
    Copy images into folders organized by year, month, and date the image was taken, while preserving the original timestamps.
    Also handle file name conflicts to avoid overwriting existing files.

    :param images: List of image file paths.
    :param output_directory: Directory where organized folders will be created.
    :param progress_callback: Callback function to update progress.
    """
    file_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    total_images = len(images)
    for i, image_path in enumerate(images):
        date_taken, filename = get_image_metadata(image_path)
        if date_taken:
            year = date_taken.year
            month = date_taken.month
            day = date_taken.day
            file_metadata[year][month][day].append((image_path, filename))
        progress_callback(i + 1, total_images)

    for year, month_data in file_metadata.items():
        year_folder = os.path.join(output_directory, str(year))
        os.makedirs(year_folder, exist_ok=True)
        for month, day_data in month_data.items():
            month_folder = os.path.join(year_folder, f"{month:02d}")
            os.makedirs(month_folder, exist_ok=True)
            for day, files in day_data.items():
                day_folder = os.path.join(month_folder, f"{day:02d}")
                os.makedirs(day_folder, exist_ok=True)
                for source_path, filename in files:
                    destination_path = os.path.join(day_folder, filename)
                    if os.path.exists(destination_path):
                        # Handle file name conflicts
                        name, ext = os.path.splitext(filename)
                        i = 1
                        while os.path.exists(os.path.join(day_folder, f"{name}_{i}{ext}")):
                            i += 1
                        destination_path = os.path.join(day_folder, f"{name}_{i}{ext}")
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied '{source_path}' to '{destination_path}'")

class ImageOrganizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Organizer")
        self.geometry("600x400")

        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()

        self.progress_var = tk.IntVar()
        self.progress_label = None

        self.create_widgets()

    def create_widgets(self):
        # Input directory selection
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Input Directory:").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.input_directory, width=40).pack(side=tk.LEFT)
        tk.Button(input_frame, text="Browse", command=self.select_input_directory).pack(side=tk.LEFT)

        # Output directory selection
        output_frame = tk.Frame(self)
        output_frame.pack(pady=10)
        tk.Label(output_frame, text="Output Directory:").pack(side=tk.LEFT)
        tk.Entry(output_frame, textvariable=self.output_directory, width=40).pack(side=tk.LEFT)
        tk.Button(output_frame, text="Browse", command=self.select_output_directory).pack(side=tk.LEFT)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self, mode='determinate', variable=self.progress_var)
        self.progress_bar.pack(pady=10, fill=tk.X)

        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Organize Images", command=self.organize_images).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def select_input_directory(self):
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_directory.set(directory)

    def select_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)

    def update_progress(self, current, total):
        self.progress_var.set(current)
        self.progress_label.config(text=f"Processing {current} of {total} images...")

    def organize_images(self):
        input_dir = self.input_directory.get()
        output_dir = self.output_directory.get()

        if not input_dir or not output_dir:
            tk.messagebox.showerror("Error", "Please select both input and output directories.")
            return

        images = search_images(input_dir)
        self.progress_bar["maximum"] = len(images)

        copy_images_by_date(images, output_dir, self.update_progress)

        self.progress_bar["value"] = len(images)
        self.progress_label.config(text="Image organization completed.")
        tk.messagebox.showinfo("Completed", "Image organization completed.")

if __name__ == '__main__':
    app = ImageOrganizerGUI()
    app.mainloop()