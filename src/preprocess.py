import cv2
def load_and_preprocess_image(image_path):
    """
    Load and preprocess the chess board image
    """
    # Load the image
    original_image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    gaussian_blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Apply Otsu's thresholding
    _, otsu_binary = cv2.threshold(gaussian_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    return original_image, otsu_binary
