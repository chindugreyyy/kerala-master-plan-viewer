#!/usr/bin/env python3
"""
Kerala Master Plan Georeferencing Pipeline

This script automates the georeferencing process once control points are identified.

Usage:
1. First, identify control points (landmarks) on the map
2. Create a CSV file with control points (see sample_gcp.csv)
3. Run: python3 georeference_pipeline.py --city thiruvananthapuram --gcp-file gcp.csv
4. Output: GeoTIFF and COG files

Requirements:
- GDAL (brew install gdal)
- Python 3.8+

Example GCP CSV format:
mapX,mapY,worldX,worldY,worldZ,landmark
100,200,76.9525,8.4875,0,Thiruvananthapuram Central Railway Station
300,400,76.9436,8.4828,0,Padmanabhaswamy Temple
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data-processing" / "map-pages"
OUTPUT_DIR = BASE_DIR / "data-processing" / "georeferenced"
OUTPUT_DIR.mkdir(exist_ok=True)

# City configurations
CITIES = {
    "thiruvananthapuram": {
        "name": "Thiruvananthapuram",
        "map_page": "thiruvananthapuram/thiruvananthapuram_page_008.png",
        "bounds": [76.80, 8.30, 77.10, 8.60],  # [minX, minY, maxX, maxY]
        "crs": "EPSG:4326",
        "sample_gcp": [
            # (mapX, mapY, lon, lat, name)
            (100, 200, 76.9525, 8.4875, "Thiruvananthapuram Central Railway Station"),
            (300, 400, 76.9436, 8.4828, "Padmanabhaswamy Temple"),
            (500, 600, 76.9492, 8.5058, "Kerala Secretariat"),
            (700, 800, 76.9561, 8.5083, "Napier Museum"),
        ]
    },
    "kochi": {
        "name": "Kochi",
        "map_page": "kochi/kochi_page_008.png",
        "bounds": [76.15, 9.85, 76.45, 10.15],
        "crs": "EPSG:4326",
        "sample_gcp": [
            (100, 200, 76.2828, 9.9836, "Ernakulam Junction Railway Station"),
            (300, 400, 76.2425, 9.9667, "Fort Kochi"),
            (500, 600, 76.2781, 9.9831, "Marine Drive"),
            (700, 800, 76.3075, 10.0269, "Lulu Mall"),
        ]
    },
    "kozhikode": {
        "name": "Kozhikode",
        "map_page": "kozhikode/kozhikode_page_009.png",
        "bounds": [75.65, 11.15, 75.95, 11.45],
        "crs": "EPSG:4326",
        "sample_gcp": [
            (100, 200, 75.7808, 11.2486, "Kozhikode Railway Station"),
            (300, 400, 75.7811, 11.2586, "Mananchira Square"),
            (500, 600, 75.7708, 11.2575, "Kozhikode Beach"),
            (700, 800, 75.6925, 11.3881, "Kappad Beach"),
        ]
    }
}

def run_gdal_command(cmd):
    """Run a GDAL command and check output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def create_vrt(input_file, output_file):
    """Create a VRT file with georeferencing"""
    cmd = f"gdal_translate -of VRT -a_srs EPSG:4326 {input_file} {output_file}"
    return run_gdal_command(cmd)

def georeference_with_gcp(input_file, gcp_file, output_file):
    """
    Georeference an image using Ground Control Points
    
    GCP file format (CSV):
    mapX,mapY,worldX,worldY,worldZ,landmark
    """
    import csv
    
    # Read GCPs
    gcps = []
    with open(gcp_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            gcp = {
                'mapX': float(row['mapX']),
                'mapY': float(row['mapY']),
                'worldX': float(row['worldX']),
                'worldY': float(row['worldY']),
                'worldZ': float(row.get('worldZ', 0)),
            }
            gcps.append(gcp)
    
    print(f"Loaded {len(gcps)} control points")
    
    # Build GCP string for gdal_translate
    gcp_str = ""
    for gcp in gcps:
        gcp_str += f" -gcp {gcp['mapX']} {gcp['mapY']} {gcp['worldX']} {gcp['worldY']} {gcp['worldZ']}"
    
    # Step 1: Add GCPs to image
    temp_file = output_file.parent / f"{output_file.stem}_with_gcp.tif"
    cmd = f"gdal_translate -of GTiff -a_srs EPSG:4326{gcp_str} {input_file} {temp_file}"
    if not run_gdal_command(cmd):
        return False
    
    # Step 2: Apply polynomial transformation
    cmd = f"gdalwarp -of GTiff -t_srs EPSG:4326 -r bilinear -order 2 {temp_file} {output_file}"
    if not run_gdal_command(cmd):
        return False
    
    # Clean up temp file
    temp_file.unlink(missing_ok=True)
    
    return True

def convert_to_cog(input_file, output_file):
    """Convert GeoTIFF to Cloud Optimized GeoTIFF"""
    cmd = f"""gdal_translate \
        -of COG \
        -co COMPRESS=DEFLATE \
        -co RESAMPLING=AVERAGE \
        -co OVERVIEW_RESAMPLING=AVERAGE \
        -co BLOCKSIZE=512 \
        -co QUALITY=85 \
        {input_file} {output_file}"""
    
    return run_gdal_command(cmd)

def validate_cog(cog_file):
    """Validate a COG file"""
    cmd = f"gdalinfo {cog_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "LAYOUT=COG" in result.stdout:
        print("✅ Valid COG file")
        return True
    else:
        print("⚠️  May not be a valid COG")
        return False

def generate_info(city_key, geotiff_file, cog_file):
    """Generate information about the georeferenced file"""
    cmd = f"gdalinfo {geotiff_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    info = {
        "city": CITIES[city_key]["name"],
        "geotiff": str(geotiff_file),
        "cog": str(cog_file),
        "size_mb": round(os.path.getsize(cog_file) / (1024 * 1024), 2),
        "gdal_info": result.stdout
    }
    
    return info

def create_sample_gcp(city_key, output_file):
    """Create a sample GCP CSV file"""
    city = CITIES[city_key]
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['mapX', 'mapY', 'worldX', 'worldY', 'worldZ', 'landmark'])
        
        for gcp in city['sample_gcp']:
            writer.writerow([gcp[0], gcp[1], gcp[2], gcp[3], 0, gcp[4]])
    
    print(f"Created sample GCP file: {output_file}")
    print("⚠️  IMPORTANT: These are sample coordinates!")
    print("You need to identify actual landmarks on the map and update the coordinates.")
    print("See GEOREFERENCING.md for detailed instructions.")

def main():
    parser = argparse.ArgumentParser(description='Kerala Master Plan Georeferencing Pipeline')
    parser.add_argument('--city', choices=list(CITIES.keys()), required=True,
                       help='City to georeference')
    parser.add_argument('--gcp-file', type=str, help='Path to GCP CSV file')
    parser.add_argument('--create-sample-gcp', action='store_true',
                       help='Create a sample GCP file for the city')
    parser.add_argument('--skip-georeference', action='store_true',
                       help='Skip georeferencing (use existing GeoTIFF)')
    parser.add_argument('--geotiff', type=str, help='Path to existing GeoTIFF')
    
    args = parser.parse_args()
    
    city_key = args.city
    city = CITIES[city_key]
    
    print(f"="*60)
    print(f"Kerala Master Plan Georeferencing Pipeline")
    print(f"City: {city['name']}")
    print(f"Map: {city['map_page']}")
    print(f"="*60)
    
    # Check if GDAL is available
    result = subprocess.run("gdalinfo --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ GDAL not found. Install with: brew install gdal")
        sys.exit(1)
    print(f"✅ GDAL: {result.stdout.strip()}")
    
    # Create sample GCP if requested
    if args.create_sample_gcp:
        sample_file = BASE_DIR / f"{city_key}_sample_gcp.csv"
        create_sample_gcp(city_key, sample_file)
        return
    
    # Check input file
    input_file = DATA_DIR / city['map_page']
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        print(f"Make sure the map page has been extracted.")
        sys.exit(1)
    print(f"✅ Input file: {input_file}")
    
    # Output files
    city_output_dir = OUTPUT_DIR / city_key
    city_output_dir.mkdir(exist_ok=True)
    
    geotiff_file = city_output_dir / f"{city_key}_georeferenced.tif"
    cog_file = city_output_dir / f"{city_key}_cog.tif"
    
    # Georeference
    if not args.skip_georeference:
        if not args.gcp_file:
            print("❌ No GCP file specified. Use --gcp-file or --create-sample-gcp")
            sys.exit(1)
        
        gcp_file = Path(args.gcp_file)
        if not gcp_file.exists():
            print(f"❌ GCP file not found: {gcp_file}")
            sys.exit(1)
        
        print(f"\n🗺️  Georeferencing with {gcp_file}...")
        if not georeference_with_gcp(input_file, gcp_file, geotiff_file):
            print("❌ Georeferencing failed")
            sys.exit(1)
        print(f"✅ GeoTIFF created: {geotiff_file}")
    else:
        if not args.geotiff:
            print("❌ No GeoTIFF specified. Use --geotiff")
            sys.exit(1)
        geotiff_file = Path(args.geotiff)
    
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
    print(f"Georeferencing Complete!")
    print(f"{'='*60}")
    print(f"City: {info['city']}")
    print(f"GeoTIFF: {info['geotiff']}")
    print(f"COG: {info['cog']}")
    print(f"Size: {info['size_mb']} MB")
    print(f"\nNext steps:")
    print(f"1. Upload COG to Cloudflare R2")
    print(f"2. Update cities.json with the URL")
    print(f"3. Deploy to Vercel")
    print(f"{'='*60}")

if __name__ == "__main__":
    import csv
    main()
