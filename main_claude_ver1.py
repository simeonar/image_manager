import os
import shutil
from datetime import datetime
from typing import List
from PIL import Image, ExifTags, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog

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

def copy_images_by_date(images: List[str], output_directory: str) -> None:
    """
    Copy images into folders organized by date the image was taken,
    while preserving the original timestamps.

    :param images: List of image file paths.
    :param output_directory: Directory where organized folders will be created.
    """
    for image_path in images:
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                date_folder = ''

                if exif_data:
                    date_time_original_tag = next(
                        (ExifTags.TAGS[k] for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'DateTimeOriginal'),
                        None)
                    if date_time_original_tag and date_time_original_tag in exif_data:
                        date_taken = exif_data[date_time_original_tag]
                        date_str = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').date()
                        date_folder = os.path.join(output_directory, str(date_str))
                    else:
                        print(f"No 'DateTimeOriginal' found in EXIF for {image_path}, using last modified date.")

                if not date_folder:  # If no EXIF or date wasn't found, default to the file's last modified time
                    last_modified_time = os.path.getmtime(image_path)
                    date_str = datetime.fromtimestamp(last_modified_time).date()
                    date_folder = os.path.join(output_directory, f"LastModified_{date_str}")

                os.makedirs(date_folder, exist_ok=True)
                destination_path = os.path.join(date_folder, os.path.basename(image_path))
                shutil.copy2(image_path, destination_path)  # copy2 retains metadata including timestamps
                print(f"Copied '{image_path}' to '{date_folder}'")

        except UnidentifiedImageError:
            print(f"Cannot identify image file {image_path}, skipping.")
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

def select_directory(title: str) -> str:
    """
    Open a dialog to select a directory.

    :param title: Title for the directory selection dialog.
    :return: The selected directory path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    selected_directory = filedialog.askdirectory(title=title)
    return selected_directory

def main() -> None:
    """
    Main function to execute the image manager functionalities.
    """
    # Select directory to search for images
    directory = select_directory("Select Directory to Search for Images")
    if not directory:
        print("Image directory selection cancelled.")
        return

    # Select directory to store organized images by date
    output_directory = select_directory("Select Directory to Store Organized Images")
    if not output_directory:
        print("Output directory selection cancelled.")
        return

    # Search for images
    images = search_images(directory)

    # Copy images organized by date taken while preserving timestamps
    copy_images_by_date(images, output_directory)

if __name__ == '__main__':
    main()