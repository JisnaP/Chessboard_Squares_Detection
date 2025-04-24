import cv2
import numpy as np

def detect_edges_and_contours(binary_image):
    """
    Detect edges and contours in the binary image
    """
    # Edge detection using Canny
    canny = cv2.Canny(binary_image, 20, 255)
    
    # Dilate the edges
    kernel = np.ones((5, 5), np.uint8)
    img_dilation = cv2.dilate(canny, kernel, iterations=1)
    lines = cv2.HoughLinesP(img_dilation, 1, np.pi/180, threshold=200, minLineLength=200, maxLineGap=100)

    if lines is not None:
     for i, line in enumerate(lines):
        x1, y1, x2, y2 = line[0]

        # draw lines
        cv2.line(img_dilation, (x1, y1), (x2, y2), (255,255,255), 2)

    kernel = np.ones((3, 3), np.uint8)
    # Additional dilation for contour detection
    img_dilation_2 = cv2.dilate(img_dilation, kernel, iterations=1)
    
    # Find contours
    board_contours, _ = cv2.findContours(img_dilation_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return board_contours, img_dilation_2
def extract_squares(board_contours, area_min=20, area_max=10000):
    """
    Extract square coordinates from contours
    """
    square_centers = []
    
    for contour in board_contours:
        area = cv2.contourArea(contour)
        if area_min < area < area_max:
            # Approximate the contour to a simpler shape
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Ensure the approximated contour has 4 points (quadrilateral)
            if len(approx) == 4:
                pts = [pt[0] for pt in approx]  # Extract coordinates
                
                # Define the points explicitly
                pt1 = tuple(pts[0])
                pt2 = tuple(pts[1])
                pt3 = tuple(pts[2])
                pt4 = tuple(pts[3])
                
                # Calculate center
                x, y, w, h = cv2.boundingRect(contour)
                center_x = (x+(x+w))/2
                center_y = (y+(y+h))/2

                square_centers.append([center_x, center_y, pt2, pt1, pt3, pt4])
    sorted_coordinates = sorted(square_centers, key=lambda x: x[1], reverse=True)
    return sorted_coordinates
def count_squares_by_color(sorted_coordinates, binary_image):
    """
    Count white and black squares based on average color.
    """
    white_count = 0
    black_count = 0
    avg_colors = []
    square_details = []

    #  compute average colors
    for coordinate in sorted_coordinates:
        points = coordinate[2:]  # Get only the tuple points
        
        # Extract x and y coordinates from the points
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        
        # Determine the bounding box of the rectangle
        x_min = int(min(x_coords))
        x_max = int(max(x_coords))
        y_min = int(min(y_coords))
        y_max = int(max(y_coords))
        
        # Extract the rectangle from the binary image
        rectangle = binary_image[y_min:y_max, x_min:x_max]
        
        # Calculate the average color of the rectangle
        avg_color = np.mean(rectangle)
        avg_colors.append(avg_color)

    # Compute threshold after collecting all averages
    thres = np.mean(avg_colors) if avg_colors else 127  

    #  classify each square
    for i, coordinate in enumerate(sorted_coordinates):
        points = coordinate[2:]
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        x_min = int(min(x_coords))
        x_max = int(max(x_coords))
        y_min = int(min(y_coords))
        y_max = int(max(y_coords))
        rectangle = binary_image[y_min:y_max, x_min:x_max]
        avg_color = np.mean(rectangle)

        if avg_color < thres:
            black_count += 1
            color_label = "black"
        else:
            white_count += 1
            color_label = "white"

        square_details.append({
            'bounds': (x_min, y_min, x_max, y_max),
            'avg_color': avg_color,
            'color_label': color_label
        })

    return white_count, black_count, square_details
