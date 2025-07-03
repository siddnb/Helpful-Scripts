#!/usr/bin/env python3
import typer
import subprocess
import os
import sys
from pathlib import Path
import time

app = typer.Typer()

'''
This function takes all the images in a given directory and resizes them, adding these new smaller images
to the target_directory.
If the source_directory doesn't exist, or the target_directory already exists, throw an error
'''
@app.command()
def generate_previews(source_directory: Path, target_directory: Path, max_size: int):
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

            # Copy and resize the image to the target directory
            command = ["sips", "-Z", str(max_size), os.path.join(source_directory, filename), "--out", dst_path]
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

'''
This function removes the images from the target directory that are not in the source directory
e.g. if the source directory has images a.jpg, b.jpg and the target directory has images a.jpg, b.jpg, b.DNG, c.jpg, c.DNG
the function will remove c.DNG and c.jpg from the target directory
'''
@app.command()
def clean_up_originals(source_directory: Path, target_directory: Path, raw_extension: str = ".DNG", compressed_extension: str = ".jpg"):
    # Check if directories exist
    if not source_directory.is_dir():
        raise FileNotFoundError(f"Source directory '{source_directory}' does not exist.")
    if not target_directory.is_dir():
        raise FileNotFoundError(f"Target directory '{target_directory}' does not exist.")

    # Get list of base filenames (without extensions) from source directory
    source_files = set()
    for file_path in source_directory.iterdir():
        if file_path.suffix.lower() == compressed_extension.lower():
            source_files.add(file_path.stem)

    # Check each file in target directory
    # First identify files to be removed
    files_to_remove = []
    total_files = 0
    for file_path in target_directory.iterdir():
        if (file_path.suffix.lower() == raw_extension.lower() or 
            file_path.suffix.lower() == compressed_extension.lower()):
            total_files += 1
            if file_path.stem not in source_files:
                files_to_remove.append(file_path)

    # Prompt user before deletion
    if files_to_remove:
        print(f"\nFound {len(files_to_remove)} files to remove out of {total_files} total files.")
        print("\nFiles to be removed:")
        for file_path in files_to_remove:
            print(f"- {file_path.name}")
        
        response = input("\nDo you want to proceed with deletion? (y/N): ").lower()
        if response != 'y':
            print("Aborted. No files were deleted.")
            return
            
        # Proceed with deletion
        files_removed = 0
        removed_files = []
        for file_path in files_to_remove:
            removed_files.append(str(file_path.name))
            file_path.unlink()
            files_removed += 1
    else:
        files_removed = 0
        removed_files = []

    print(f"\n=== Cleanup Summary ===")
    print(f"Files removed: {files_removed}")
    if files_removed > 0:
        print("\nRemoved files:")
        for file in removed_files:
            print(f"- {file}")

if __name__ == "__main__":
    app()