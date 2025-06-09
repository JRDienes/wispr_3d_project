# WISPR 3D Visualization Project

This project creates a 3D spherical visualization of NASA's Parker Solar Probe WISPR (Wide-field Imager for Solar Probe) images. The visualization shows the time evolution of the WISPR data in a spherical format with a yellow/orange color scheme.

## Features

- 3D spherical visualization of WISPR FITS images
- Time-series animation of multiple WISPR observations
- Custom color mapping (yellow/orange)
- Automatic data normalization and smoothing
- Support for multiple FITS files

## Requirements

- Python 3.x
- Required packages (see requirements.txt):
  - numpy
  - astropy
  - matplotlib
  - scipy
  - imageio
  - scikit-image

## Installation

1. Clone this repository:
```bash
git clone https://github.com/JRDienes/wispr_3d_project.git
cd wispr_3d_project
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your WISPR FITS files in the `wispr_data` directory
2. Run the visualization script:
```bash
python wispr_3d_visualization.py
```

The script will generate a GIF animation in the `output` directory.

## Output

The script generates a GIF file (`wispr_time_series_visualization.gif`) in the `output` directory that shows the time evolution of the WISPR data in a 3D spherical format.

## Data Source

The WISPR images are from NASA's Parker Solar Probe mission. The FITS files contain the raw image data from the WISPR instrument.

## License

This project is open source and available under the MIT License. 