# WISPR 3D Visualization

This project creates 3D rotating visualizations from NASA Parker Solar Probe WISPR FITS images.

## Requirements

- Python 3.7 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your WISPR FITS image in the project directory
2. Edit the `wispr_3d_visualization.py` file to update the `fits_file` path to point to your FITS image
3. Run the script:
```bash
python wispr_3d_visualization.py
```

The script will create a 3D rotating visualization of your WISPR image and save it as a GIF in the `output` directory.

## Features

- Loads FITS format images
- Creates a 3D surface plot of the image data
- Generates a smooth rotating animation
- Saves the result as a color GIF
- Applies Gaussian smoothing for better visualization
- Normalizes the data for optimal display

## Output

The script will create a GIF file named `wispr_3d_visualization.gif` in the `output` directory. The visualization includes:
- A 3D surface plot where the height represents the intensity of the image
- A full 360-degree rotation
- Color mapping using the 'viridis' colormap
- Smooth animation with 180 frames 