import cv2
import numpy as np
import os
import random

def encrypt(original_image, images_to_encrypt, dataset_folder, encrypted_folder):
    # Path for the original image
    original_image_path = os.path.join(dataset_folder, original_image)
    img1 = cv2.imread(original_image_path)
    if img1 is None:
        print(f"Error: Original image {original_image_path} not found or unable to read.")
        return

    # Ensure encrypted directory exists
    if not os.path.exists(encrypted_folder):
        os.makedirs(encrypted_folder)

    for idx, image_file in enumerate(images_to_encrypt, start=1):
        # Path for the image to be encrypted
        image_to_encrypt_path = os.path.join(dataset_folder, image_file)
        img2 = cv2.imread(image_to_encrypt_path)
        if img2 is None:
            print(f"Error: Image {image_to_encrypt_path} not found or unable to read.")
            continue

        # Encryption process
        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for l in range(3):
                    v1 = format(img1[i][j][l], '08b')
                    v2 = format(img2[i][j][l], '08b')
                    v3 = v1[:4] + v2[:4]
                    img1[i][j][l] = int(v3, 2)

        # Save the encrypted image
        encrypted_image_path = os.path.join(encrypted_folder, f'encrypted_{idx}.png')
        cv2.imwrite(encrypted_image_path, img1)

def decrypt(encrypted_image, decrypted_folder, file_id):
    img = cv2.imread(encrypted_image)
    if img is None:
        print("Error: Encrypted image not found or unable to read.")
        return

    width = img.shape[0]
    height = img.shape[1]
    decrypted_img = np.zeros((width, height, 3), np.uint8)

    for i in range(width):
        for j in range(height):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4
                decrypted_img[i][j][l] = int(v3, 2)

    cv2.imwrite(os.path.join(decrypted_folder, f'decrypted_{file_id}.png'), decrypted_img)

def autodecrypt(encrypted_folder, decrypted_folder):
    if not os.path.exists(decrypted_folder):
        os.makedirs(decrypted_folder)

    encrypted_files = [f for f in os.listdir(encrypted_folder) if os.path.isfile(os.path.join(encrypted_folder, f))]

    for file_id, file_name in enumerate(encrypted_files, start=1):
        encrypted_image_path = os.path.join(encrypted_folder, file_name)
        decrypt(encrypted_image_path, decrypted_folder, file_id)

# Main driver
dataset_folder = 'dataset'
encrypted_folder = 'encrypted_images'
decrypted_folder = 'decrypted_images'

original_image = 'image1.jpg'
images_to_encrypt = ['image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg']
encrypt(original_image, images_to_encrypt, dataset_folder, encrypted_folder)

# Automatically decrypt all images in the encrypted_images folder
autodecrypt(encrypted_folder, decrypted_folder)
