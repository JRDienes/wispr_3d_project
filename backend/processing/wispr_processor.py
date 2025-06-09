import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from skimage.transform import resize
import matplotlib.pyplot as plt
from pathlib import Path
import json
from datetime import datetime

class WISPRProcessor:
    def __init__(self, target_shape=(1024, 960)):
        self.target_shape = target_shape
        self.output_dir = Path("backend/data/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_fits_file(self, file_path):
        """Process a FITS file and return normalized data."""
        with fits.open(file_path) as hdul:
            data = hdul[0].data
            header = hdul[0].header
            
            # Get timestamp
            time_str = header.get('DATE-OBS', '')
            try:
                timestamp = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                timestamp = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        
        # Downsample to target shape
        data = resize(data, self.target_shape, anti_aliasing=True)
        
        # Normalize data
        data = self.normalize_data(data)
        
        # Apply smoothing
        data = gaussian_filter(data, sigma=1)
        
        return data, timestamp
    
    def normalize_data(self, data):
        """Normalize data to 0-1 range."""
        data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
        data_min = np.min(data)
        data_max = np.max(data)
        norm = (data - data_min) / (data_max - data_min)
        return np.clip(norm, 0, 1)
    
    def generate_preview(self, data, output_path):
        """Generate a preview image of the data."""
        plt.figure(figsize=(10, 10))
        plt.imshow(data, cmap='YlOrRd')
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    
    def process_directory(self, input_dir):
        """Process all FITS files in a directory."""
        input_dir = Path(input_dir)
        processed_data = []
        
        for file_path in input_dir.glob("*.fits"):
            # Process the file
            data, timestamp = self.process_fits_file(file_path)
            
            # Generate preview
            preview_path = self.output_dir / f"{file_path.stem}_preview.png"
            self.generate_preview(data, preview_path)
            
            # Save processed data
            data_path = self.output_dir / f"{file_path.stem}_processed.npy"
            np.save(data_path, data)
            
            processed_data.append({
                "id": file_path.stem,
                "timestamp": timestamp.isoformat(),
                "data_path": str(data_path),
                "preview_path": str(preview_path)
            })
        
        # Save metadata
        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(processed_data, f, indent=2)
        
        return processed_data

if __name__ == "__main__":
    processor = WISPRProcessor()
    processor.process_directory("backend/data/wispr_data") 