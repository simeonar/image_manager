import os
import shutil
from datetime import datetime
from typing import List
from PIL import Image
import argparse


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
    return images


def copy_images_by_date(images: List[str], output_directory: str) -> None:
    """
    Copy images into folders organized by date the image was taken.

    :param images: List of image file paths.
    :param output_directory: Directory where organized folders will be created.
    """
    for image_path in images:
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    date_taken = exif_data.get(36867)  # TAG: DateTimeOriginal
                    if date_taken:
                        date_str = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').date()
                        date_folder = os.path.join(output_directory, str(date_str))
                        os.makedirs(date_folder, exist_ok=True)
                        shutil.copy(image_path, date_folder)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")


def filter_images_by_size(images: List[str], size_limit: int) -> List[str]:
    """
    Filter images by file size.

    :param images: List of image file paths.
    :param size_limit: Maximum allowed file size in bytes.
    :return: List of image file paths that exceed the size limit.
    """
    large_images = [img_path for img_path in images if os.path.getsize(img_path) > size_limit]
    return large_images


def main() -> None:
    """
    Main function to execute the image manager functionalities based on user inputs.
    """
    parser = argparse.ArgumentParser(description='Image Manager Application')
    parser.add_argument('directory', type=str, help='Directory to search for images')
    parser.add_argument('output_directory', type=str, help='Directory to store organized images by date')
    args = parser.parse_args()

    # Search for images
    images = search_images(args.directory)
    print(f"Found {len(images)} images.")

    # Copy images organized by date taken
    copy_images_by_date(images, args.output_directory)

    # Example of filtering by a specific size limit, without removal functionality
    # This function might be useful to know which images are large, but doesn't remove them
    size_limit = 10048576  # Example size limit in bytes for filtering
    large_images = filter_images_by_size(images, size_limit)
    print(f"Found {len(large_images)} images larger than {size_limit} bytes.")


if __name__ == '__main__':
    main()