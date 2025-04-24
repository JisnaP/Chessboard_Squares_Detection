import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def correct_skewed_image(input_path, output_path=None, square_size=50):
    """
    Corrects a skewed chessboard image
    
    Args:
        input_path: Path to the skewed image
        output_path: Path to save the corrected image
        square_size: Size of each chess square in pixels
    
    Returns:
        The corrected image
    """
    # Load the skewed chessboard image
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError(f"Could not read image at {input_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort by area 
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    board_contour = contours[0]
    
    # Approximate the contour to get a quadrilateral
    epsilon = 0.02 * cv2.arcLength(board_contour, True)
    approx = cv2.approxPolyDP(board_contour, epsilon, True)
    
    if len(approx) == 4:
        # Order the corners
        pts = np.array([pt[0] for pt in approx], dtype='float32')
        
        # Sort the points
        def order_points(pts):
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            diff = np.diff(pts, axis=1)
            
            rect[0] = pts[np.argmin(s)]     
            rect[2] = pts[np.argmax(s)]     
            rect[1] = pts[np.argmin(diff)]  
            rect[3] = pts[np.argmax(diff)]  
            
            return rect
        
        rect = order_points(pts)
        
        dst_size = 8 * square_size  
        dst = np.array([
            [0, 0],
            [dst_size - 1, 0],
            [dst_size - 1, dst_size - 1],
            [0, dst_size - 1]
        ], dtype="float32")
        
        # Perspective transform
        #get the perspective transfrom matrix
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (dst_size, dst_size))
        
        # Save the corrected image 
        if output_path:
            plt.figure(figsize=(10, 10))
            plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.savefig(output_path, bbox_inches='tight')
            plt.close()
            print(f"Corrected image saved to {output_path}")
        
        return warped
    else:
        print("Chessboard corners not detected correctly.")
        return None

def get_default_output_path(input_path):
    """
    Generate default output path based on input filename
    """
    # Get the input filename without extension
    input_filename = os.path.splitext(os.path.basename(input_path))[0]
    
    # Create output directory if it doesn't exist
    #corrected image is saved into data folder itself
    os.makedirs('./data', exist_ok=True)
    
    # Generate output path
    return f'./data/corrected_{input_filename}.png'

if __name__ == "__main__":
    # Set up argument parser

    parser = argparse.ArgumentParser(description='Correct skewed chessboard images')
    
    # Add arguments
    parser.add_argument('--input', '-i', required=True,
                        help='Path to the skewed chessboard image')
    parser.add_argument('--output', '-o',
                        help='Path to save the corrected image (default: ./data/corrected_[input_filename].png)')
    parser.add_argument('--square_size', '-s', type=int, default=50,
                        help='Size of each chess square in pixels (default: 50)')
    
    # Parse arguments
    args = parser.parse_args()
    
    
    if args.output is None:
        args.output = get_default_output_path(args.input)
    
    
    correct_skewed_image(args.input, args.output, args.square_size)
