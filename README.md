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
git clone https://github.com/yourusername/chess-board-detection.git
cd chess-board-detection

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
python perspective_trasformation.py --input ./data/skewed_image.png
```
## License

MIT Licence

