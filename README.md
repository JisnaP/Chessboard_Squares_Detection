# Chess Board Square Detection

This project provides a modular implementation for detecting and counting white and black squares on a chess board from an image.

## Features

- Load and preprocess chess board images
- Detect edges and contours
- Extract and identify chess squares
- Count white and black squares
- Visualize detection results
- Automatic threshold testing for optimal results

## Requirements

- Python 3.10
- OpenCV (cv2)
- NumPy
- Matplotlib

## Installation

```bash
# Clone the repository (if applicable)
git clone https://github.com/JisnaP/Chessboard_Squares_Detection.git
cd Chessboard_Squares_Detection

# Install required packages
pip install -r requirements.txt
```



## How It Works

1. **Image Loading & Preprocessing**: Converts image to grayscale, applies Gaussian blur, and thresholds using Otsu's method
2. **Edge Detection**: Uses Canny edge detection followed by dilation
3. **Contour Detection**: Finds contours in the processed image
4. **Square Extraction**: Identifies quadrilaterals from the contours that likely represent chess squares
5. **Color Analysis**: Examines the average color of each detected square to classify it as white or black
6. **Visualization**: Creates a visual representation of the detected squares

## Usage
```bash
python main.py --image path_to_image --output path_to_output
```
**Example Usage**
```bash
python main.py --image ./data/chessboard.png --output ./outputs/output_image.png
```
## For distorted image run the code in the notebook foolowing the steps
## Skewed Image
If the image is skewed first apply perspective transformation. Then use the corrected image in the main function. 
```bash
python perspective_transformation.py --input ./data/skewed_image.png
```
**Note**
![partialchessboard image](https://github.com/JisnaP/Chessboard_Squares_Detection/blob/main/data/partialchessboard.png) 
For the above image approximation using rectangles is not detecting incomplete squares.It detects full squares perfectly. Approximation using Convex hull detects the border black edges as well which gives incorrect counts for black squares. 

## License

MIT Licence

