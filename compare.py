import os
import cv2
from skimage.metrics import structural_similarity as ssim

def compare_images(file1, file2):
    # Load the images
    original = cv2.imread(file1)
    altered = cv2.imread(file2)

    # Check if images are loaded
    if original is None:
        return f"Error loading original image: {file1}"
    if altered is None:
        return f"Error loading altered image: {file2}"

    # Convert the images to grayscale
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    altered_gray = cv2.cvtColor(altered, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    score, _ = ssim(original_gray, altered_gray, full=True)
    return f"SSIM score for {os.path.basename(file2)}: {score}"


# Path to the original image
original_image_path = "dataset/image1.jpg"

# Path to the directory containing all encrypted images
encrypted_images_dir = "all_encrypted_labeled"

# List to store comparison results
comparison_results = []

# Compare each encrypted image to the original image
for filename in os.listdir(encrypted_images_dir):
    encrypted_image_path = os.path.join(encrypted_images_dir, filename)
    result = compare_images(original_image_path, encrypted_image_path)
    comparison_results.append(result)

print(comparison_results)
