#!/usr/bin/env python3
"""
Rough georeferencing for Kerala master plan maps

This creates an approximate georeferencing using city bounds.
The maps will be roughly aligned but will need manual refinement.

Usage:
    python3 rough_georeference.py --city thiruvananthapuram
    python3 rough_georeference.py --city kochi
    python3 rough_georeference.py --city kozhikode

Output:
    - GeoTIFF (roughly georeferenced)
    - COG (Cloud Optimized GeoTIFF)
    - World file (.wld)
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data-processing" / "map-pages"
OUTPUT_DIR = BASE_DIR / "data-processing" / "georeferenced"
OUTPUT_DIR.mkdir(exist_ok=True)

# City bounds based on municipal corporation boundaries
# [minLon, minLat, maxLon, maxLat]
CITY_BOUNDS = {
    "thiruvananthapuram": {
        "name": "Thiruvananthapuram",
        "map_file": "thiruvananthapuram/thiruvananthapuram_page_008.png",
        "bounds": [76.80, 8.30, 77.10, 8.60],  # rough municipal area
        "crs": "EPSG:4326",
    },
    "kochi": {
        "name": "Kochi",
        "map_file": "kochi/kochi_page_008.png",
        "bounds": [76.15, 9.85, 76.45, 10.15],  # rough municipal area
        "crs": "EPSG:4326",
    },
    "kozhikode": {
        "name": "Kozhikode",
        "map_file": "kozhikode/kozhikode_page_009.png",
        "bounds": [75.65, 11.15, 75.95, 11.45],  # rough municipal area
        "crs": "EPSG:4326",
    }
}

def run_gdal_command(cmd):
    """Run a GDAL command and check output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    if result.stdout.strip():
        print(f"Output: {result.stdout}")
    return True

def create_georeferenced_tiff(input_file, output_file, bounds, img_width, img_height):
    """
    Create a georeferenced GeoTIFF using simple bounding box
    
    bounds: [minLon, minLat, maxLon, maxLat]
    """
    minLon, minLat, maxLon, maxLat = bounds
    
    # Calculate pixel size
    pixel_width = (maxLon - minLon) / img_width
    pixel_height = (minLat - maxLat) / img_height  # negative because Y goes down
    
    # Upper-left corner
    ulx = minLon
    uly = maxLat
    
    # Create world file
    wld_file = output_file.with_suffix('.wld')
    with open(wld_file, 'w') as f:
        f.write(f"{pixel_width}\n")
        f.write(f"0\n")
        f.write(f"0\n")
        f.write(f"{pixel_height}\n")
        f.write(f"{ulx}\n")
        f.write(f"{uly}\n")
    
    print(f"Created world file: {wld_file}")
    
    # Use gdal_translate to create GeoTIFF with world file
    # First, create a plain TIFF
    temp_tiff = output_file.with_suffix('.temp.tif')
    
    # Convert PNG to GeoTIFF with georeferencing
    cmd = f"""gdal_translate \
        -of GTiff \
        -a_srs EPSG:4326 \
        -a_ullr {ulx} {uly} {maxLon} {minLat} \
        -co COMPRESS=DEFLATE \
        {input_file} {temp_tiff}"""
    
    if not run_gdal_command(cmd):
        return False
    
    # Add overviews for better performance
    cmd = f"gdaladdo -r average {temp_tiff} 2 4 8 16 32"
    run_gdal_command(cmd)
    
    # Move to final location
    os.rename(temp_tiff, output_file)
    
    return True

def convert_to_cog(input_file, output_file):
    """Convert GeoTIFF to Cloud Optimized GeoTIFF"""
    cmd = f"""gdal_translate \
        -of COG \
        -co COMPRESS=DEFLATE \
        -co RESAMPLING=AVERAGE \
        -co OVERVIEW_RESAMPLING=AVERAGE \
        -co BLOCKSIZE=512 \
        {input_file} {output_file}"""
    
    return run_gdal_command(cmd)

def validate_cog(cog_file):
    """Validate a COG file"""
    cmd = f"gdalinfo {cog_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "LAYOUT=COG" in result.stdout or "COG" in result.stdout:
        print("✅ Valid COG file")
        return True
    else:
        print("⚠️  May not be a valid COG, checking further...")
        print(result.stdout[:500])
        return False

def generate_info(city_key, geotiff_file, cog_file):
    """Generate information about the georeferenced file"""
    cmd = f"gdalinfo {geotiff_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    info = {
        "city": CITY_BOUNDS[city_key]["name"],
        "geotiff": str(geotiff_file),
        "cog": str(cog_file),
        "size_mb": round(os.path.getsize(cog_file) / (1024 * 1024), 2),
        "gdal_info": result.stdout
    }
    
    return info

def main():
    parser = argparse.ArgumentParser(description='Rough georeferencing for Kerala master plans')
    parser.add_argument('--city', choices=list(CITY_BOUNDS.keys()), required=True,
                       help='City to georeference')
    parser.add_argument('--bounds', nargs=4, type=float, metavar=('MINLON', 'MINLAT', 'MAXLON', 'MAXLAT'),
                       help='Custom bounds [minLon minLat maxLon maxLat]')
    
    args = parser.parse_args()
    
    city_key = args.city
    city = CITY_BOUNDS[city_key]
    
    print(f"="*60)
    print(f"Rough Georeferencing Pipeline")
    print(f"City: {city['name']}")
    print(f"="*60)
    
    # Check if GDAL is available
    result = subprocess.run("gdalinfo --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ GDAL not found. Install with: brew install gdal")
        sys.exit(1)
    print(f"✅ GDAL: {result.stdout.strip()}")
    
    # Check input file
    input_file = DATA_DIR / city['map_file']
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    print(f"✅ Input file: {input_file}")
    
    # Get image dimensions
    img = Image.open(input_file)
    img_width, img_height = img.size
    print(f"✅ Image dimensions: {img_width}x{img_height}")
    
    # Use custom bounds if provided, otherwise use defaults
    bounds = args.bounds if args.bounds else city['bounds']
    print(f"✅ Bounds: {bounds}")
    
    # Output files
    city_output_dir = OUTPUT_DIR / city_key
    city_output_dir.mkdir(exist_ok=True)
    
    geotiff_file = city_output_dir / f"{city_key}_rough.tif"
    cog_file = city_output_dir / f"{city_key}_rough_cog.tif"
    
    # Create georeferenced GeoTIFF
    print(f"\n🗺️  Creating rough georeferencing...")
    if not create_georeferenced_tiff(input_file, geotiff_file, bounds, img_width, img_height):
        print("❌ Georeferencing failed")
        sys.exit(1)
    print(f"✅ GeoTIFF created: {geotiff_file}")
    
    # Convert to COG
    print(f"\n📦 Converting to Cloud Optimized GeoTIFF...")
    if not convert_to_cog(geotiff_file, cog_file):
        print("❌ COG conversion failed")
        sys.exit(1)
    print(f"✅ COG created: {cog_file}")
    
    # Validate
    print(f"\n🔍 Validating COG...")
    validate_cog(cog_file)
    
    # Generate info
    info = generate_info(city_key, geotiff_file, cog_file)
    
    print(f"\n{'='*60}")
    print(f"Rough Georeferencing Complete!")
    print(f"{'='*60}")
    print(f"City: {info['city']}")
    print(f"GeoTIFF: {info['geotiff']}")
    print(f"COG: {info['cog']}")
    print(f"Size: {info['size_mb']} MB")
    print(f"\n⚠️  IMPORTANT: This is a ROUGH georeferencing!")
    print(f"The map will be approximately aligned but may need manual adjustment.")
    print(f"\nNext steps:")
    print(f"1. Test the COG in QGIS or the viewer")
    print(f"2. If misaligned, create precise GCPs using the georeferencing tool")
    print(f"3. Upload to Cloudflare R2 when satisfied")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
