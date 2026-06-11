#!/usr/bin/env python3
"""
Crop black/white margins from Kerala master plan map images
and regenerate COGs with proper bounds
"""

import os
import sys
from pathlib import Path
from PIL import Image
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data-processing" / "map-pages"
OUTPUT_DIR = BASE_DIR / "data-processing" / "georeferenced"
VIEWER_DATA_DIR = BASE_DIR / "kerala-master-plan-viewer" / "data"

CITY_CONFIG = {
    "thiruvananthapuram": {
        "name": "Thiruvananthapuram",
        "map_file": "thiruvananthapuram/thiruvananthapuram_page_008.png",
        "bounds": [76.80, 8.30, 77.10, 8.60],
    },
    "kochi": {
        "name": "Kochi",
        "map_file": "kochi/kochi_page_008.png",
        "bounds": [76.15, 9.85, 76.45, 10.15],
    },
    "kozhikode": {
        "name": "Kozhikode",
        "map_file": "kozhikode/kozhikode_page_009.png",
        "bounds": [75.65, 11.15, 75.95, 11.45],
    }
}

def find_content_bounds(img_array):
    """
    Find the bounding box of actual content (non-white/non-black pixels)
    Returns: (left, top, right, bottom)
    """
    # Convert to grayscale
    if len(img_array.shape) == 3:
        gray = np.mean(img_array, axis=2)
    else:
        gray = img_array
    
    # Threshold: consider pixels that are not pure white (255) or pure black (0)
    # Use a threshold of 250 for white and 10 for black
    threshold_white = 250
    threshold_black = 10
    
    # Create mask: True for content pixels
    mask = (gray < threshold_white) & (gray > threshold_black)
    
    # Find rows and columns with content
    rows_with_content = np.where(mask.any(axis=1))[0]
    cols_with_content = np.where(mask.any(axis=0))[0]
    
    if len(rows_with_content) == 0 or len(cols_with_content) == 0:
        return None
    
    top = rows_with_content[0]
    bottom = rows_with_content[-1] + 1
    left = cols_with_content[0]
    right = cols_with_content[-1] + 1
    
    return (left, top, right, bottom)

def crop_image(input_file, output_file):
    """Crop margins from image and save"""
    img = Image.open(input_file)
    
    # Convert to RGB if necessary
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_array = np.array(img)
    
    # Find content bounds
    bounds = find_content_bounds(img_array)
    if bounds is None:
        print("No content found!")
        return None
    
    left, top, right, bottom = bounds
    
    # Add small padding (10 pixels) to avoid cutting off content
    padding = 10
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(img_array.shape[1], right + padding)
    bottom = min(img_array.shape[0], bottom + padding)
    
    # Crop
    cropped = img.crop((left, top, right, bottom))
    cropped.save(output_file, 'PNG')
    
    print(f"Cropped: {img.size} → {cropped.size}")
    print(f"Removed: {img.size[0] - cropped.size[0]}px horizontal, {img.size[1] - cropped.size[1]}px vertical")
    
    return cropped

def create_cog_from_png(input_file, output_file, bounds):
    """Create a COG from a PNG file with georeferencing"""
    # Open image
    img = Image.open(input_file)
    
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_array = np.array(img)
    img_array = np.transpose(img_array, (2, 0, 1))
    
    height, width = img_array.shape[1], img_array.shape[2]
    
    minLon, minLat, maxLon, maxLat = bounds
    transform = from_bounds(minLon, minLat, maxLon, maxLat, width, height)
    
    with rasterio.open(
        output_file,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=3,
        dtype=img_array.dtype,
        crs='EPSG:4326',
        transform=transform,
        compress='deflate',
        tiled=True,
        blockxsize=512,
        blockysize=512,
    ) as dst:
        dst.write(img_array)
        
        # Build overviews
        factors = [2, 4, 8, 16, 32]
        dst.build_overviews(factors, Resampling.average)
    
    print(f"✅ Created COG: {output_file}")
    print(f"   Size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
    
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', choices=list(CITY_CONFIG.keys()), required=True)
    args = parser.parse_args()
    
    city_key = args.city
    city = CITY_CONFIG[city_key]
    
    print(f"="*60)
    print(f"Cropping and regenerating COG for {city['name']}")
    print(f"="*60)
    
    input_file = DATA_DIR / city['map_file']
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    # Create temp directory
    temp_dir = OUTPUT_DIR / city_key
    temp_dir.mkdir(exist_ok=True)
    
    # Crop the image
    print(f"\n✂️  Cropping margins...")
    cropped_file = temp_dir / f"{city_key}_cropped.png"
    cropped = crop_image(input_file, cropped_file)
    
    if cropped is None:
        print("❌ Cropping failed")
        sys.exit(1)
    
    # Create COG from cropped image
    print(f"\n📦 Creating COG...")
    cog_file = temp_dir / f"{city_key}_cog.tif"
    if not create_cog_from_png(cropped_file, cog_file, city['bounds']):
        print("❌ COG creation failed")
        sys.exit(1)
    
    # Copy to viewer
    print(f"\n📁 Copying to viewer...")
    VIEWER_DATA_DIR.mkdir(exist_ok=True)
    viewer_cog = VIEWER_DATA_DIR / f"{city_key}_cog.tif"
    import shutil
    shutil.copy(cog_file, viewer_cog)
    print(f"✅ Copied to: {viewer_cog}")
    
    print(f"\n{'='*60}")
    print(f"✅ Done! Cropped COG created for {city['name']}")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"1. Test in viewer: https://kerala-master-plan-viewer.vercel.app")
    print(f"2. If alignment is still off, adjust bounds in cities.json")
    print(f"3. Redeploy: vercel --yes --prod")

if __name__ == "__main__":
    main()
