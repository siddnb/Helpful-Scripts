#!/usr/bin/env python3

import subprocess
import os
import sys
import time

'''
This function takes all the images in a given directory and resizes them, adding these new smaller images
to the target_directory.
If the source_directory doesn't exist, or the target_directory already exists, throw an error
'''
def resize_images(source_directory, target_directory, size):
    
    # Check if source_directory exists
    if not os.path.isdir(source_directory):
        raise FileNotFoundError(f"Source directory '{source_directory}' does not exist.")
    # Check if target_directory already exists
    if os.path.exists(target_directory):
        raise FileExistsError(f"Target directory '{target_directory}' already exists.")
    # Create the target directory
    os.makedirs(target_directory)
    # Supported image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
    
    # Start timing
    start_time = time.time()
    converted_count = 0
    
    # Process each image in the source directory
    for filename in os.listdir(source_directory):
        if filename.lower().endswith(image_extensions):
            dst_path = os.path.join(target_directory, filename)
            # Resize the image in the target directory
            command = ["sips", "-Z", str(size), os.path.join(source_directory, filename), "--out", dst_path]
            subprocess.run(command, check=True)
            converted_count += 1
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Print summary statistics
    print(f"\n=== Conversion Summary ===")
    print(f"Images converted: {converted_count}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    if converted_count > 0:
        print(f"Average time per image: {elapsed_time/converted_count:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python image_processing.py <source_directory> <target_directory> <size>")
        print("\nArguments:")
        print("  source_directory  : Directory containing the original images")
        print("  target_directory  : Directory where resized images will be saved")
        print("  size             : Maximum dimension (width or height) in pixels")
        print("\nExample:")
        print("  python image_processing.py ./original_images ./resized_images 800")
        sys.exit(1)
    source_directory = sys.argv[1]
    target_directory = sys.argv[2]
    size = sys.argv[3]

    resize_images(source_directory, target_directory, size)