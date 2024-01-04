import cv2
import numpy as np
import os

def encrypt_lsb(original_image, images_to_encrypt, dataset_folder, encrypted_folder):
    original_image_path = os.path.join(dataset_folder, original_image)
    img1 = cv2.imread(original_image_path)
    if img1 is None:
        print(f"Error: Original image {original_image_path} not found or unable to read.")
        return

    if not os.path.exists(encrypted_folder):
        os.makedirs(encrypted_folder)

    for idx, image_file in enumerate(images_to_encrypt, start=1):
        image_to_encrypt_path = os.path.join(dataset_folder, image_file)
        img2 = cv2.imread(image_to_encrypt_path)
        if img2 is None:
            print(f"Error: Image {image_to_encrypt_path} not found or unable to read.")
            continue

        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for l in range(3):
                    # Replace the LSB of img1 with the MSB of img2
                    img1[i][j][l] = (img1[i][j][l] & ~1) | (img2[i][j][l] >> 7)

        encrypted_image_path = os.path.join(encrypted_folder, f'encrypted_{idx}.png')
        cv2.imwrite(encrypted_image_path, img1)

def decrypt_lsb(encrypted_image, decrypted_folder, file_id):
    img = cv2.imread(encrypted_image)
    if img is None:
        print("Error: Encrypted image not found or unable to read.")
        return

    width, height = img.shape[:2]
    decrypted_img = np.zeros((width, height, 3), np.uint8)

    for i in range(width):
        for j in range(height):
            for l in range(3):
                # Retrieve the LSB and shift it to the MSB position
                decrypted_img[i][j][l] = (img[i][j][l] & 1) << 7

    cv2.imwrite(os.path.join(decrypted_folder, f'decrypted_{file_id}.png'), decrypted_img)

def autodecrypt(encrypted_folder, decrypted_folder):
    if not os.path.exists(decrypted_folder):
        os.makedirs(decrypted_folder)

    encrypted_files = [f for f in os.listdir(encrypted_folder) if os.path.isfile(os.path.join(encrypted_folder, f))]

    for file_id, file_name in enumerate(encrypted_files, start=1):
        encrypted_image_path = os.path.join(encrypted_folder, file_name)
        decrypt_lsb(encrypted_image_path, decrypted_folder, file_id)

# Main driver
dataset_folder = 'dataset'
encrypted_folder = 'encrypted_images'
decrypted_folder = 'decrypted_images'

original_image = 'image1.jpg'
images_to_encrypt = ['image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg']

encrypt_lsb(original_image, images_to_encrypt, dataset_folder, encrypted_folder)
autodecrypt(encrypted_folder, decrypted_folder)
