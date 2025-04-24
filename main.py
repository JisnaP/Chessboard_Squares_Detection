import argparse
import matplotlib.pyplot as plt
import cv2
import os
from src.preprocess import load_and_preprocess_image
from src.contour import detect_edges_and_contours, count_squares_by_color, extract_squares
from src.visualization import visualize_detected_squares

def main(image_path,output_path=None):
    """
    Main function to run the chess board square detection
    """
    # Load and preprocess image
    original_image, binary_image = load_and_preprocess_image(image_path)
    
    # Detect edges and contours
    board_contours, processed_image = detect_edges_and_contours(binary_image)
    
    # Extract squares
    sorted_coordinates = extract_squares(board_contours)
    
    # Count squares by color
    white_count, black_count, square_details = count_squares_by_color(
        sorted_coordinates, binary_image
    )
    
    # Create visualization
    visualization = visualize_detected_squares(original_image, square_details)
    
    # Display results
    print(f"White squares: {white_count}")
    print(f"Black squares: {black_count}")
    print(f"Total squares: {white_count + black_count}")
    
    # If output path is specified, save the visualization
    if output_path:
        # Display images
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        plt.title("Original Image")
        plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        
        plt.subplot(2, 2, 2)
        plt.title("Binary Image")
        plt.imshow(binary_image, cmap='gray')
        
        plt.subplot(2, 2, 3)
        plt.title("Processed Image")
        plt.imshow(processed_image, cmap='gray')
        
        plt.subplot(2, 2, 4)
        plt.title(f"Detected Squares (W:{white_count}, B:{black_count})")
        plt.imshow(cv2.cvtColor(visualization, cv2.COLOR_BGR2RGB))
        
        plt.tight_layout()
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Output saved to {output_path}")
            
    return {
        'original_image': original_image,
        'binary_image': binary_image,
        'processed_image': processed_image,
        'visualization': visualization,
        'white_count': white_count,
        'black_count': black_count,
        'square_details': square_details
    }

def get_default_output_path(input_path):
    """
    Generate default output path based on input filename
    """
    # Get the input filename without extension
    input_filename = os.path.splitext(os.path.basename(input_path))[0]
    
    # Create output directory if it doesn't exist
    os.makedirs('./outputs', exist_ok=True)
    
    # Generate output path
    return f'./outputs/output_{input_filename}.png'

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Chess board square detection')
    
    # Add arguments
    parser.add_argument('--image', '-i', required=True, 
                        help='Path to the input image')
    parser.add_argument('--output', '-o', 
                        help='Path to save the output visualization (default: ./outputs/output_[input_filename].png)')
    
    
    # Parse arguments
    args = parser.parse_args()
    
    
    if args.output is None:
        args.output = get_default_output_path(args.image)
    
    # Run main function 
    results = main(args.image,  args.output)