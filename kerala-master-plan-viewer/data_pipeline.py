#!/usr/bin/env python3
"""
Kerala Master Plan Data Pipeline Helper

This script helps with:
1. Converting scanned PDFs to GeoTIFFs
2. Georeferencing using GCP (Ground Control Points)
3. Converting to Cloud Optimized GeoTIFF (COG)
4. Validating output files

Requirements:
    pip install gdal rasterio pillow

Or install GDAL system-wide:
    Ubuntu/Debian: sudo apt-get install gdal-bin python3-gdal
    macOS: brew install gdal
    Windows: https://www.gisinternals.com/

Usage:
    python data_pipeline.py --input scanned_plan.pdf --output cog_plan.tif --gcp gcp.csv
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_gdal():
    """Check if GDAL is installed."""
    try:
        result = subprocess.run(['gdalinfo', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ GDAL found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ GDAL not found. Please install GDAL:")
    print("   macOS: brew install gdal")
    print("   Ubuntu: sudo apt-get install gdal-bin")
    print("   Windows: https://www.gisinternals.com/")
    return False


def pdf_to_tiff(input_pdf, output_tiff, dpi=300):
    """Convert PDF to GeoTIFF using gdal_translate."""
    print(f"\n📄 Converting PDF to TIFF (DPI={dpi})...")
    
    cmd = [
        'gdal_translate',
        '-of', 'GTiff',
        '-outsize', str(dpi * 10), str(dpi * 10),  # Approximate size
        input_pdf,
        output_tiff
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Converted: {output_tiff}")
        return True
    else:
        print(f"❌ Conversion failed: {result.stderr}")
        return False


def add_gcp(input_tiff, output_tiff, gcp_file):
    """
    Add Ground Control Points to georeference the image.
    
    GCP file format (CSV):
        pixel_x,pixel_y,longitude,latitude
        100,200,76.9366,8.5241
        500,400,76.9400,8.5300
        ...
    """
    print(f"\n🎯 Adding Ground Control Points...")
    
    # Read GCPs
    gcps = []
    with open(gcp_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            if len(parts) == 4:
                px, py, lon, lat = map(float, parts)
                gcps.append(f"-gcp {px} {py} {lon} {lat}")
    
    if not gcps:
        print("❌ No valid GCPs found in file")
        return False
    
    # Build gdal_translate command
    cmd = ['gdal_translate', '-of', 'GTiff'] + gcps + [input_tiff, output_tiff]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Added {len(gcps)} GCPs: {output_tiff}")
        return True
    else:
        print(f"❌ Failed: {result.stderr}")
        return False


def warp_to_epsg4326(input_tiff, output_tiff):
    """Warp to EPSG:4326 (WGS 84) standard projection."""
    print(f"\n🌐 Warping to EPSG:4326 (WGS 84)...")
    
    cmd = [
        'gdalwarp',
        '-t_srs', 'EPSG:4326',
        '-r', 'bilinear',
        '-of', 'GTiff',
        input_tiff,
        output_tiff
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Warped: {output_tiff}")
        return True
    else:
        print(f"❌ Failed: {result.stderr}")
        return False


def convert_to_cog(input_tiff, output_cog, compress='WEBP', quality=80):
    """
    Convert GeoTIFF to Cloud Optimized GeoTIFF.
    
    Args:
        compress: WEBP (best compression), LZW (most compatible), or DEFLATE
        quality: 1-100 for WEBP
    """
    print(f"\n☁️ Converting to Cloud Optimized GeoTIFF (compression={compress})...")
    
    cmd = [
        'gdal_translate',
        '-of', 'COG',
        '-co', f'COMPRESS={compress}',
        '-co', 'OVERVIEW_RESAMPLING=BILINEAR',
    ]
    
    if compress == 'WEBP':
        cmd.extend(['-co', f'QUALITY={quality}'])
    
    cmd.extend([input_tiff, output_cog])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ COG created: {output_cog}")
        return True
    else:
        print(f"❌ Failed: {result.stderr}")
        return False


def validate_cog(cog_file):
    """Validate that a file is a proper COG."""
    print(f"\n🔍 Validating COG...")
    
    cmd = ['gdalinfo', cog_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Cannot read file: {result.stderr}")
        return False
    
    info = result.stdout
    
    checks = {
        'Is GeoTIFF': 'Driver: GTiff' in info,
        'Has overviews': 'Overviews' in info,
        'Is COG': 'LAYOUT=COG' in info or 'LAYOUT=IFDS_BEFORE_DATA' in info,
        'Has CRS': 'Coordinate System' in info,
    }
    
    all_pass = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
        if not passed:
            all_pass = False
    
    return all_pass


def get_file_info(tiff_file):
    """Get basic file information."""
    print(f"\n📊 File Information:")
    
    cmd = ['gdalinfo', '-nomd', '-noct', tiff_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        for line in lines:
            if any(key in line for key in ['Size', 'Coordinate System', 'Origin', 'Pixel Size', 'Corner Coordinates']):
                print(f"  {line}")
    
    # File size
    size = os.path.getsize(tiff_file)
    print(f"  File size: {size / (1024*1024):.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description='Kerala Master Plan Data Pipeline Helper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline: PDF → GeoTIFF → COG
  python data_pipeline.py --input plan.pdf --output plan_cog.tif --gcp gcp.csv

  # Just convert to COG
  python data_pipeline.py --input plan.tif --output plan_cog.tif --only-cog

  # Validate existing COG
  python data_pipeline.py --validate existing_cog.tif
        """
    )
    
    parser.add_argument('--input', '-i', help='Input file (PDF or TIFF)')
    parser.add_argument('--output', '-o', help='Output COG file')
    parser.add_argument('--gcp', '-g', help='Ground Control Points CSV file')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for PDF conversion (default: 300)')
    parser.add_argument('--compress', default='WEBP', choices=['WEBP', 'LZW', 'DEFLATE', 'NONE'],
                        help='COG compression method (default: WEBP)')
    parser.add_argument('--quality', type=int, default=80, help='WEBP quality 1-100 (default: 80)')
    parser.add_argument('--only-cog', action='store_true', help='Only convert existing TIFF to COG')
    parser.add_argument('--validate', '-v', help='Validate an existing COG file')
    parser.add_argument('--info', help='Show info about a TIFF file')
    
    args = parser.parse_args()
    
    # Check GDAL
    if not check_gdal():
        sys.exit(1)
    
    # Validate mode
    if args.validate:
        validate_cog(args.validate)
        return
    
    # Info mode
    if args.info:
        get_file_info(args.info)
        return
    
    # Full pipeline
    if not args.input or not args.output:
        parser.print_help()
        sys.exit(1)
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
    
    # Create temp directory
    temp_dir = Path('temp_georeferencing')
    temp_dir.mkdir(exist_ok=True)
    
    try:
        if args.only_cog:
            # Skip to COG conversion
            temp_tiff = input_path
            cog_file = output_path
        else:
            # Step 1: PDF to TIFF
            if input_path.suffix.lower() == '.pdf':
                temp_tiff = temp_dir / f"{input_path.stem}_converted.tif"
                if not pdf_to_tiff(str(input_path), str(temp_tiff), args.dpi):
                    sys.exit(1)
            else:
                temp_tiff = input_path
            
            # Step 2: Add GCPs
            if args.gcp:
                if not Path(args.gcp).exists():
                    print(f"❌ GCP file not found: {args.gcp}")
                    sys.exit(1)
                
                gcp_tiff = temp_dir / f"{input_path.stem}_gcp.tif"
                if not add_gcp(str(temp_tiff), str(gcp_tiff), args.gcp):
                    sys.exit(1)
                temp_tiff = gcp_tiff
                
                # Step 3: Warp to EPSG:4326
                warped_tiff = temp_dir / f"{input_path.stem}_warped.tif"
                if not warp_to_epsg4326(str(temp_tiff), str(warped_tiff)):
                    sys.exit(1)
                temp_tiff = warped_tiff
            else:
                print("⚠️ No GCP file provided. Skipping georeferencing.")
                print("   Output will not be properly aligned with map.")
        
        # Step 4: Convert to COG
        cog_file = output_path
        if not convert_to_cog(str(temp_tiff), str(cog_file), args.compress, args.quality):
            sys.exit(1)
        
        # Step 5: Validate
        if validate_cog(str(cog_file)):
            print(f"\n✅ Success! COG ready: {cog_file}")
            get_file_info(str(cog_file))
            print(f"\n📋 Next steps:")
            print(f"   1. Upload to cloud storage (R2/S3)")
            print(f"   2. Get public URL")
            print(f"   3. Update cities.json")
        else:
            print(f"\n⚠️ Validation failed. Check output file.")
            
    finally:
        # Cleanup temp files
        if not args.only_cog:
            print(f"\n🧹 Cleaning temp files...")
            for f in temp_dir.glob(f"{input_path.stem}_*.tif"):
                f.unlink()
            if not any(temp_dir.iterdir()):
                temp_dir.rmdir()


if __name__ == '__main__':
    main()
