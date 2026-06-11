#!/usr/bin/env python3
"""
Make white background transparent and create proper COGs

This script:
1. Loads the map PNG
2. Makes white/gray background pixels transparent
3. Saves as RGBA
4. Creates COG with alpha channel
5. Copies to viewer directory
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

def make_transparent(input_file, output_file, threshold=250):
    """
    Make white/gray background transparent
    
    threshold: pixels with R, G, B all > threshold become transparent
    """
    img = Image.open(input_file)
    
    # Convert to RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    arr = np.array(img)
    
    # Create mask: True for background pixels (all channels > threshold)
    # For RGBA, we check R, G, B channels
    background_mask = (arr[:,:,0] > threshold) & (arr[:,:,1] > threshold) & (arr[:,:,2] > threshold)
    
    # Also check near-white pixels (slightly lower threshold for anti-aliased edges)
    background_mask2 = (arr[:,:,0] > 240) & (arr[:,:,1] > 240) & (arr[:,:,2] > 240)
    
    # Combine masks
    background_mask = background_mask | background_mask2
    
    # Set alpha to 0 for background pixels
    arr[background_mask, 3] = 0
    
    # Keep non-background pixels at alpha=255
    arr[~background_mask, 3] = 255
    
    # Save
    result = Image.fromarray(arr)
    result.save(output_file, 'PNG')
    
    # Stats
    total_pixels = background_mask.size
    bg_pixels = np.sum(background_mask)
    print(f"Made {bg_pixels}/{total_pixels} pixels ({bg_pixels/total_pixels*100:.1f}%) transparent")
    
    return output_file

def create_cog_rgba(input_file, output_file, bounds):
    """Create a COG from RGBA PNG with georeferencing"""
    img = Image.open(input_file)
    
    # Ensure RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    arr = np.array(img)
    
    # Transpose to (bands, height, width) for rasterio
    # For RGBA: bands = 4 (R, G, B, A)
    img_array = np.transpose(arr, (2, 0, 1))
    
    height, width = img_array.shape[1], img_array.shape[2]
    
    minLon, minLat, maxLon, maxLat = bounds
    transform = from_bounds(minLon, minLat, maxLon, maxLat, width, height)
    
    with rasterio.open(
        output_file,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=4,  # RGBA
        dtype=img_array.dtype,
        crs='EPSG:4326',
        transform=transform,
        compress='deflate',
        tiled=True,
        blockxsize=512,
        blockysize=512,
        nodata=0,  # Transparent pixels are nodata
    ) as dst:
        dst.write(img_array)
        
        # Build overviews
        factors = [2, 4, 8, 16, 32]
        dst.build_overviews(factors, Resampling.average)
    
    print(f"✅ Created RGBA COG: {output_file}")
    print(f"   Size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
    
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', choices=list(CITY_CONFIG.keys()), required=True)
    parser.add_argument('--threshold', type=int, default=250, help='White threshold (default: 250)')
    args = parser.parse_args()
    
    city_key = args.city
    city = CITY_CONFIG[city_key]
    
    print(f"="*60)
    print(f"Creating transparent COG for {city['name']}")
    print(f"="*60)
    
    input_file = DATA_DIR / city['map_file']
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    # Create output directory
    temp_dir = OUTPUT_DIR / city_key
    temp_dir.mkdir(exist_ok=True)
    
    # Step 1: Make white background transparent
    print(f"\n🎨 Making white background transparent (threshold={args.threshold})...")
    transparent_file = temp_dir / f"{city_key}_transparent.png"
    make_transparent(input_file, transparent_file, args.threshold)
    
    # Step 2: Create COG with alpha
    print(f"\n📦 Creating RGBA COG...")
    cog_file = temp_dir / f"{city_key}_cog.tif"
    if not create_cog_rgba(transparent_file, cog_file, city['bounds']):
        print("❌ COG creation failed")
        sys.exit(1)
    
    # Step 3: Copy to viewer
    print(f"\n📁 Copying to viewer...")
    VIEWER_DATA_DIR.mkdir(exist_ok=True)
    viewer_cog = VIEWER_DATA_DIR / f"{city_key}_cog.tif"
    import shutil
    shutil.copy(cog_file, viewer_cog)
    print(f"✅ Copied to: {viewer_cog}")
    
    print(f"\n{'='*60}")
    print(f"✅ Done! Transparent COG created for {city['name']}")
    print(f"{'='*60}")
    print(f"\nThe white background should now be transparent.")
    print(f"Test in viewer: https://kerala-master-plan-viewer.vercel.app")

if __name__ == "__main__":
    main()
