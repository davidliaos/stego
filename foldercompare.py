import os
import cv2
from skimage.metrics import structural_similarity as ssim

def compare_images(file1, file2, output_file):
    # Load the images
    original = cv2.imread(file1, cv2.IMREAD_GRAYSCALE)
    altered = cv2.imread(file2, cv2.IMREAD_GRAYSCALE)

    # Check if images are loaded
    if original is None or altered is None:
        error_message = f"Error loading images: {file1} or {file2}"
        with open(output_file, 'a') as file:
            file.write(error_message + '\n')
        return error_message

    # Compute SSIM between the two images
    score = ssim(original, altered)
    result = f"SSIM score between {os.path.basename(file1)} and {os.path.basename(file2)}: {score:.4f}"
    with open(output_file, 'a') as file:
        file.write(result + '\n')
    return result


# Path to the directories containing bitplanes
original_bitplanes_dir = "./bitplanes/original"
encrypted_bitplanes_dir = "./bitplanes/encrypted"

# Output file to store comparison results
output_file = "bitplanecomparrison.txt"

# Clear the content of the output file if it exists or create it if it doesn't
open(output_file, 'w').close()

# Compare each bitplane of the original image with the corresponding bitplane of the encrypted image
for i in range(1, 9):
    original_bitplane_path = os.path.join(original_bitplanes_dir, f"image1_bitplane{i}.png")
    encrypted_bitplane_path = os.path.join(encrypted_bitplanes_dir, f"res3_encrypted_1_bitplane{i}.png")
    print(compare_images(original_bitplane_path, encrypted_bitplane_path, output_file))
