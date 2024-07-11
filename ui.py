import tkinter as tk
from tkinter import filedialog
import cv2

def select_image():
    
    root = tk.Tk()
    root.withdraw() 
    
    # display dialog box to open image and get file path
    filename = filedialog.askopenfilename()
    print(f"Selected file: {filename}")
    return filename

#function to retrieve image resolution
def get_res(path):
    img = cv2.imread(path)
    height, width, _ = img.shape
    cv2.imwrite('C:\Project\AVVR-Pipeline-Internship\edgenet360\Data\Input\\rgb.png', img)

    return height, width

# selected_image_path = select_image()
# print("Selected Image Path:", selected_image_path)
# print("resolution:", get_res(selected_image_path))