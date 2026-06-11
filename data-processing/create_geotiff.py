#!/usr/bin/env python3
"""
Create georeferenced GeoTIFFs and COGs using rasterio

Usage:
    python3 create_geotiff.py --city thiruvananthapuram
    python3 create_geotiff.py --city kochi
    python3 create_geotiff.py --city kozhikode
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data-processing" / "map-pages"
OUTPUT_DIR = BASE_DIR / "data-processing" / "georeferenced"
OUTPUT_DIR.mkdir(exist_ok=True)

# City bounds [minLon, minLat, maxLon, maxLat]
CITY_BOUNDS = {
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

def create_geotiff(input_file, output_file, bounds):
    """Create a georeferenced GeoTIFF from PNG"""
    # Open image
    img = Image.open(input_file)
    
    # Convert to RGB if necessary
    if img.mode == 'RGBA':
        # Create white background for alpha
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Transpose to (bands, height, width) for rasterio
    img_array = np.transpose(img_array, (2, 0, 1))
    
    height, width = img_array.shape[1], img_array.shape[2]
    
    # Create transform from bounds
    minLon, minLat, maxLon, maxLat = bounds
    transform = from_bounds(minLon, minLat, maxLon, maxLat, width, height)
    
    # Write GeoTIFF
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
    
    print(f"✅ Created GeoTIFF: {output_file}")
    print(f"   Dimensions: {width}x{height}")
    print(f"   Bounds: {bounds}")
    print(f"   Size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
    
    return True

def create_cog(input_file, output_file):
    """Create a Cloud Optimized GeoTIFF"""
    # Copy the file first
    import shutil
    shutil.copy(input_file, output_file)
    
    # Add overviews (pyramid levels)
    with rasterio.open(output_file, 'r+') as dst:
        # Build overviews
        factors = [2, 4, 8, 16, 32]
        dst.build_overviews(factors, Resampling.average)
        
        # Update tags to indicate COG
        dst.update_tags(ns='IMAGE_STRUCTURE', COMPRESSION='DEFLATE')
        
        # Copy tile metadata
        dst.update_tags(ns='TILED', YES='YES')
        
        print(f"✅ Created COG: {output_file}")
        print(f"   Overviews: {factors}")
        print(f"   Size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Create georeferenced GeoTIFFs and COGs')
    parser.add_argument('--city', choices=list(CITY_BOUNDS.keys()), required=True,
                       help='City to process')
    
    args = parser.parse_args()
    
    city_key = args.city
    city = CITY_BOUNDS[city_key]
    
    print(f"="*60)
    print(f"Georeferencing Pipeline (Rasterio)")
    print(f"City: {city['name']}")
    print(f"="*60)
    
    # Check input file
    input_file = DATA_DIR / city['map_file']
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    print(f"✅ Input file: {input_file}")
    
    # Output files
    city_output_dir = OUTPUT_DIR / city_key
    city_output_dir.mkdir(exist_ok=True)
    
    geotiff_file = city_output_dir / f"{city_key}_georeferenced.tif"
    cog_file = city_output_dir / f"{city_key}_cog.tif"
    
    # Create georeferenced GeoTIFF
    print(f"\n🗺️  Creating georeferenced GeoTIFF...")
    if not create_geotiff(input_file, geotiff_file, city['bounds']):
        print("❌ Failed to create GeoTIFF")
        sys.exit(1)
    
    # Create COG
    print(f"\n📦 Creating Cloud Optimized GeoTIFF...")
    if not create_cog(geotiff_file, cog_file):
        print("❌ Failed to create COG")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"✅ Georeferencing Complete!")
    print(f"{'='*60}")
    print(f"GeoTIFF: {geotiff_file}")
    print(f"COG: {cog_file}")
    print(f"\n⚠️  IMPORTANT: This is a ROUGH georeferencing!")
    print(f"The map will be approximately aligned but may need manual adjustment.")
    print(f"\nNext steps:")
    print(f"1. Test the COG in the viewer")
    print(f"2. If misaligned, create precise GCPs")
    print(f"3. Upload to Cloudflare R2 when satisfied")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
