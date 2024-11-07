# Image Organizer

The Image Organizer is a desktop application that helps you organize your image files by the date they were taken. It can extract the date information from the image EXIF data or use the file's last modified date if the EXIF data is not available.

## Features

1. **Input Directory Selection**: The user can select the directory containing the images they want to organize.

2. **Output Directory Selection**: The user can select the directory where the organized images will be saved.

3. **Simple Copy Option**: The user can choose to copy the images directly to the output directory without creating date-based folders. This is useful if the user just wants to copy the files without the additional organization.

4. **Date-based Folder Organization**: If the simple copy option is not selected, the application will create folders in the output directory based on the year, month, and day the images were taken. This helps keep the organized files structured and easy to navigate.

5. **File Name Conflict Handling**: If there are any file name conflicts (i.e., two images with the same name), the application will automatically rename the newer file by adding a "copy_" prefix to the file name.

6. **Progress Tracking**: The application displays a progress bar and a label that shows the current progress of the image organization process.

7. **Comprehensive Error Handling**: The application can handle various types of errors that may occur during the image processing, such as unidentified image formats or missing EXIF data.

## How to Use

1. Launch the Image Organizer application.
2. Click the "Browse" button next to the "Input Directory" field and select the directory containing the images you want to organize.
3. Click the "Browse" button next to the "Output Directory" field and select the directory where you want the organized images to be saved.
4. (Optional) Check the "Simple copy (no date folders)" checkbox if you want to copy the images directly to the output directory without creating date-based folders.
5. Click the "Organize Images" button to start the image organization process.
6. Monitor the progress bar and the progress label to see the status of the operation.
7. Once the process is complete, a message box will inform you that the organization is finished.

## Technical Details

The Image Organizer is built using Python and the Tkinter library for the graphical user interface. It utilizes the Pillow (PIL) library to extract the EXIF data from the image files and the built-in `os` and `shutil` modules to perform file operations.

The key functions and modules used in the application are:

- `search_images`: Recursively searches for image files in the specified directory.
- `get_image_metadata`: Extracts the date the image was taken from the EXIF data or uses the file's last modified date if EXIF data is not available.
- `copy_images_by_date`: Copies the images to the output directory, organizing them by year, month, and day. It also handles file name conflicts.
- `ImageOrganizerGUI`: The main Tkinter-based application class that provides the user interface and handles the image organization process.

If you have any questions or encounter any issues, please feel free to reach out.