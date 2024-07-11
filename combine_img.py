import numpy as np
import imageio
import os
from ui import get_res

#makes sure value of x stays within the range of min and max value to prevent out of bound values accses for the image
def clamp(x, min_val, max_val):
    return max(min_val, min(x, max_val))

#clamps the floating point coordinates to nearest integer value, copies pixel value from the image to the nearest int coord
def nearest_neighbour_interpolation(img, x, y):
    h, w, _ = img.shape
    x, y = clamp(int(x), 0, w-1), clamp(int(y), 0, h-1)
    return img[y, x]


# def orientation_to_face(x, y, z):
#     abs_x, abs_y, abs_z = abs(x), abs(y), abs(z)
#     if abs_x >= abs_y and abs_x >= abs_z:
#         if x > 0:
#             return 'front', -y / abs_x, -z / abs_x
#         else:
#             return 'back', y / abs_x, -z / abs_x
#     elif abs_y >= abs_x and abs_y >= abs_z:
#         if y > 0:
#             return 'right', -x / abs_y, -z / abs_y
#         else:
#             return 'left', x / abs_y, -z / abs_y
#     else:
#         if z > 0:
#             return 'top', x / abs_z, y / abs_z
#         else:
#             return 'bottom', -x / abs_z, y / abs_z

#maps the 3d coords for cube faces to 2d coords on that cube face
#finds out which cube face corresponds to the current pixel for which the 3d coords are calculated and calcs the normalised 2d coords on that face
def orientation_to_face(x, y, z):
    abs_x, abs_y, abs_z = abs(x), abs(y), abs(z)
    if abs_x >= abs_y and abs_x >= abs_z:
        if x > 0:
            return 'frontrgb', -y / abs_x, -z / abs_x
        else:
            return 'backrgb', y / abs_x, -z / abs_x
    elif abs_y >= abs_x and abs_y >= abs_z:
        if y > 0:
            return 'rightrgb', -x / abs_y, -z / abs_y
        else:
            return 'leftrgb', x / abs_y, -z / abs_y
    else:
        if z > 0:
            return 'toprgb', x / abs_z, y / abs_z
        else:
            return 'bottomrgb', -x / abs_z, y / abs_z

#converts cube maps into omnidirectional image
def cubemap_to_omnidirectional(cube_faces, out_width, out_height):
    omnidirectional = np.zeros((out_height, out_width, 3), dtype=np.uint8)
    
    #iterates through the pixels in o/p image, for each pixel calulates spherical coord used to map 2d pixel loc to 3d points on a sphere
    #which are then converted to 3d cartesian coord to find which face of cube map current pixel corresponds to
    for j in range(out_height):
        theta = j / out_height * np.pi
        for i in range(out_width):
            phi = i / out_width * 2 * np.pi
            x = np.sin(theta) * np.cos(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(theta)
            
            face, xf, yf = orientation_to_face(x, y, z)
            face_img = cube_faces[face] #holds what cubeface and the 2d point the 3d cord maps onto
            face_size = face_img.shape[0]
            
            #converts 2d coords on cube face to pixel coords on 
            u = (xf + 1) * face_size / 2
            v = (yf + 1) * face_size / 2
            
            #get pixel value from the cubemap image and assign it to actual pixel in the omnidirectional image
            omnidirectional[j, i] = nearest_neighbour_interpolation(face_img, u, v)
    
    return omnidirectional

# if __name__ == "__main__":
#     # Load the cubemap images
#     cube_faces_dir = input("Enter the directory containing the cubemap images: ").strip()
#     faces = ["right", "left", "top", "bottom", "front", "back"]
#     cube_faces = {}
    
#     for face in faces:
#         cube_faces[face] = imageio.imread(os.path.join(cube_faces_dir, f"{face}.jpg"))



if __name__ == "__main__":
    # Load the cubemap images
    #cube_faces_dir = input("Enter the directory containing the cubemap images: ").strip()
    cube_faces_dir = "C:\Project\AVVR-Pipeline-Internship\material_recognition\Dynamic-Backward-Attention-Transformer\output\split_output"

    #faces = ["right", "left", "top", "bottom", "front", "back"]
    faces = ["rightrgb", "leftrgb", "toprgb", "bottomrgb", "frontrgb", "backrgb"]
    cube_faces = {}
    
    for face in faces:
        image_path = os.path.join(cube_faces_dir, f"{face}.png")
        image_data = imageio.imread(image_path)
        
        #rotate top and bottom face by 90 deg
        # if face in ["top", "bottom"]:
        #     image_data = np.rot90(image_data, 1)
        
        # #flip the top, bottom, front and back faces in horizontal direction
        # if face not in ["left", "right"]:
        #     image_data = image_data[:, ::-1]

        if face in ["toprgb", "bottomrgb"]:
            image_data = np.rot90(image_data, 1)
        
        if face not in ["leftrgb", "rightrgb"]:
            image_data = image_data[:, ::-1]
        
        
        cube_faces[face] = image_data

    
    # output_width = int(input("Enter output omnidirectional width: "))
    # output_height = int(input("Enter output omnidirectional height: "))
    with open('path.txt', 'r') as file:
        input_path = file.readline()
        print(f'path = {input_path}')
    os.remove('path.txt')
    height, width = get_res(input_path)
    print(height, width)
    
    output_width = width
    output_height = height

    #print(f"height: {height}, width: {width}")
    omnidirectional_img = cubemap_to_omnidirectional(cube_faces, output_width, output_height)
    
    output_path = "C:\Project\AVVR-Pipeline-Internship\edgenet360\Data\Input\material.png"
    imageio.v2.imsave(output_path, omnidirectional_img)
    print(f"Omnidirectional image saved to {output_path}")
