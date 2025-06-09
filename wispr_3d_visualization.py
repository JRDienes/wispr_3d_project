import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio
from scipy.ndimage import gaussian_filter
import os
import glob
from datetime import datetime
from skimage.transform import resize

def load_fits_image(file_path, target_shape=(1024, 960)):
    """Load a FITS image, downsample to target_shape, and return the data."""
    with fits.open(file_path) as hdul:
        data = hdul[0].data
        # Get the observation time from the header
        time_str = hdul[0].header.get('DATE-OBS', '')
        try:
            obs_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            obs_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
    # Downsample the data to target_shape
    data = resize(data, target_shape, anti_aliasing=True)
    print(f"Loaded {file_path} with shape: {data.shape}")
    return data, obs_time

def normalize_data(data):
    """Normalize the data to 0-1 range and sanitize it."""
    data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    data_min = np.min(data)
    data_max = np.max(data)
    norm = (data - data_min) / (data_max - data_min)
    norm = np.clip(norm, 0, 1)
    return norm

def create_time_series_visualization(fits_files, output_path, num_frames=60):
    """
    Create a time-series 3D spherical visualization of the WISPR images.
    
    Parameters:
    -----------
    fits_files : list
        List of paths to FITS files
    output_path : str
        Path to save the output GIF
    num_frames : int
        Number of frames in the animation
    """
    # Load all FITS files and sort by time
    data_series = []
    times = []
    for file_path in fits_files:
        data, obs_time = load_fits_image(file_path)
        data_series.append(data)
        times.append(obs_time)
    
    # Sort by time
    sorted_indices = np.argsort(times)
    data_series = [data_series[i] for i in sorted_indices]
    times = [times[i] for i in sorted_indices]
    
    # Create figure and 3D axis
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create spherical coordinates
    phi = np.linspace(0, np.pi, data_series[0].shape[0])
    theta = np.linspace(0, 2*np.pi, data_series[0].shape[1])
    phi, theta = np.meshgrid(phi, theta, indexing='ij')
    
    # Convert to Cartesian coordinates
    r = 1.0  # Radius of the sphere
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    # Create colormap (yellow/orange)
    cmap = plt.cm.YlOrRd
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    title = ax.set_title('')
    
    # Set equal aspect ratio
    ax.set_box_aspect([1,1,1])
    
    # Set the initial view
    ax.view_init(elev=30, azim=0)
    
    # Store frames for GIF
    frames = []
    
    # Create frames
    for i in range(num_frames):
        # Calculate which data point to show
        data_idx = int((i / num_frames) * len(data_series))
        if data_idx >= len(data_series):
            data_idx = len(data_series) - 1
        
        # Clear previous plot
        ax.clear()
        
        # Prepare data
        normalized_data = normalize_data(data_series[data_idx])
        smoothed_data = gaussian_filter(normalized_data, sigma=1)
        if smoothed_data.shape != phi.shape:
            smoothed_data = smoothed_data.T
        smoothed_data = np.nan_to_num(smoothed_data, nan=0.0, posinf=0.0, neginf=0.0)
        smoothed_data = np.clip(smoothed_data, 0, 1)
        colors = cmap(smoothed_data)
        colors = np.ascontiguousarray(colors, dtype=np.float32)
        
        # Plot surface
        ax.plot_surface(x, y, z, facecolors=colors, rcount=100, ccount=100, linewidth=0, antialiased=True)
        
        # Update the title with the time
        ax.set_title(f'WISPR Spherical Visualization\nTime: {times[data_idx].strftime("%Y-%m-%d %H:%M:%S")}')
        
        # Set labels and view
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_box_aspect([1,1,1])
        ax.view_init(elev=30, azim=0)
        
        # Convert plot to image
        fig.canvas.draw()
        frame = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(frame)
    
    plt.close()
    
    # Save frames as GIF
    imageio.mimsave(output_path, frames, fps=20, loop=0)

def main():
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Directory containing the WISPR FITS files
    fits_dir = 'wispr_data'
    # Pattern to match WISPR FITS files
    fits_pattern = os.path.join(fits_dir, '*.fits')
    
    # Get all matching FITS files
    fits_files = sorted(glob.glob(fits_pattern))
    
    if not fits_files:
        print(f"No FITS files found in {fits_dir} directory.")
        print("Please download the WISPR FITS files and place them in the 'wispr_data' directory.")
        return
    
    output_gif = 'output/wispr_time_series_visualization.gif'
    
    try:
        # Create the time-series visualization
        create_time_series_visualization(fits_files, output_gif, num_frames=60)
        print(f"Visualization saved to {output_gif}")
        print(f"Processed {len(fits_files)} FITS files")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 