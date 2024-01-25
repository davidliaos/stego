import cv2
import numpy as np
import os

def int2bitarray(img):
    return [np.binary_repr(pixel, width=8) for row in img for pixel in row]

def save_bitplanes(img_path):
    img = cv2.imread(img_path, 0)
    bit_array = np.array(int2bitarray(img))
    bit_array = bit_array.reshape(img.shape)

    # Extracting base filename without extension
    base_filename = os.path.splitext(os.path.basename(img_path))[0]

    for k in range(8):
        # Creating bit plane (starting from least significant bit)
        plane = np.array([[int(pixel[k]) for pixel in row] for row in bit_array], dtype=np.uint8) * 255

        # Save with corrected naming convention
        filename = f'{base_filename}_bitplane{k+1}.png'
        cv2.imwrite(filename, plane)
        print(f'Bit plane {k+1} done and saved as {filename}!')

save_bitplanes('./all_encrypted_labeled/res3_encrypted_1.png')
#save_bitplanes('./dataset/image1.jpg')
