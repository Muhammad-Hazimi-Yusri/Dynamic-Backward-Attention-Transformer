###### This code has been Referenced from: https://github.com/jaxry/panorama-to-cubemap/blob/gh-pages/convert.js


import numpy as np
import imageio
import os
from ui import select_image

#makes sure value of x stays within the range of min and max value to prevent out of bound values accses for the image
def clamp(x, min_val, max_val):
    return max(min_val, min(x, max_val))

#calculates modulus of x w.r.t n, so that ouput is always +ve
def mod(x, n):
    return ((x % n) + n) % n

#clamps the floating point coordinates to nearest integer value, copies pixel value from the image to the nearest int coord
def nearest_neigbour_interpolation(img, x, y):
    h, w, _ = img.shape
    x, y = clamp(int(x), 0, w-1), clamp(int(y), 0, h-1)
    return img[y, x]

#gives the 3d direction based on the face of the cube and x,y corrds on that face for a particular point
def orient_face(face, x, y, out):
    if face == 'front':
        out[0], out[1], out[2] = 1, x, -y
    elif face == 'back':
        out[0], out[1], out[2] = -1, -x, -y
    elif face == 'right':
        out[0], out[1], out[2] = -x, 1, -y
    elif face == 'left':
        out[0], out[1], out[2] = x, -1, -y
    elif face == 'top':
        out[0], out[1], out[2] = -y, -x, 1
    elif face == 'bottom':
        out[0], out[1], out[2] = y, -x, -1

#converts a eqirectangular image into cube faces, does 2d representation of one face of 3d map
#maps 2d coords to 3d direction then uses it to calculate spherical coords
#spherical coords are used to find/map corresponding 2d equirectanglar image coords
def face_rendering(img, face, face_size):
    out_face = np.zeros((face_size, face_size, 3), dtype=np.uint8)
    for x in range(face_size):
        for y in range(face_size):
            out = [0, 0, 0]
            orient_face(face, (2 * (x + 0.5) / face_size - 1), (2 * (y + 0.5) / face_size - 1), out)
            r = np.sqrt(out[0]**2 + out[1]**2 + out[2]**2)
            longitude = mod(np.arctan2(out[1], out[0]), 2 * np.pi)
            latitude = np.arccos(out[2] / r)
            s_x, s_y = img.shape[1] * longitude / (2 * np.pi) - 0.5, img.shape[0] * latitude / np.pi - 0.5
            out_face[y, x] = nearest_neigbour_interpolation(img, s_x, s_y)
    return out_face

#generates 6 cube faces
def generate_cube_faces(input_path, output_path="cube_faces_output"):
    
    img = imageio.imread(input_path)

    face_size = 512  #each face o/p image will be 512x512
    faces = ["right", "left", "top", "bottom", "front", "back"]
    
    results = {}
    for face in faces:
        results[face] = face_rendering(img, face, face_size)
        face_output_path = os.path.join(output_path, f"{face}.png")
        imageio.imsave(face_output_path, results[face])
        print(f"Saved {face} face to {face_output_path}")
    
    


# if __name__ == "__main__":
#     input_path = select_image()
#     height, width = get_res(input_path)
#     print("width: , Height:", width, height)
#     #output_path = input("Enter output directory: ").strip()
#     #if not output_path:
#     output_path = "C:\Project\AV-VR\material_recognition\Dynamic-Backward-Attention-Transformer\split_output"
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
#     generate_cube_faces(input_path, output_path)
        

input_path = select_image()
with open('path.txt', 'w') as file:
    file.write(input_path)
    file.close()

#output_path = input("Enter output directory: ").strip()
#if not output_path:
output_path = "C:\Project\AV-VR\material_recognition\Dynamic-Backward-Attention-Transformer\split_output"
if not os.path.exists(output_path):
    os.makedirs(output_path)
generate_cube_faces(input_path, output_path)








