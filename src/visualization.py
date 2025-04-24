import matplotlib.pyplot as plt
import cv2
def visualize_detected_squares(original_image, square_details):
    """
    Visualize the detected squares on the original image
    """
    visualization = original_image.copy()
    
    for square in square_details:
        x_min, y_min, x_max, y_max = square['bounds']
        
        # Set color based on label (green for white squares, red for black squares)
        if square['color_label'] == 'white':
            color = (0, 255, 0)  # Green
        else:
            color = (0, 0, 255)  # Red
            
        # Draw rectangle
        cv2.rectangle(visualization, (x_min, y_min), (x_max, y_max), color, 2)
        
        # Add average color value as text
        cv2.putText(visualization, f"{square['avg_color']:.1f}", 
                    (x_min, y_min-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    return visualization