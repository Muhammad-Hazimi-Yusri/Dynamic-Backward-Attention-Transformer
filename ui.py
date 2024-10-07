import tkinter as tk
from tkinter import filedialog
import cv2
import os

def select_image():
    root = tk.Tk()
    root.withdraw() 
    
    # display dialog box to open image and get file path
    filename = filedialog.askopenfilename()
    print(f"Selected file: {filename}")
    return filename

def get_res(path):
    img = cv2.imread(path)
    height, width, _ = img.shape
    
    # Get the directory two levels up from the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    
    # Construct the output path dynamically
    output_path = os.path.join(base_dir, 'edgenet360', 'Data', 'Input', 'rgb.png')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cv2.imwrite(output_path, img)

    return height, width

# selected_image_path = select_image()
# print("Selected Image Path:", selected_image_path)
# print("resolution:", get_res(selected_image_path))