#!/usr/bin/env python3
"""
Identify map pages from extracted PDF pages based on file size
"""

import os
from pathlib import Path

BASE_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/extracted-pages')

# Threshold for considering a page as a map (large image)
MAP_SIZE_THRESHOLD = 5_000_000  # 5 MB

cities = {
    'Thiruvananthapuram': 'thiruvananthapuram',
    'Kochi': 'kochi',
    'Kozhikode': 'kozhikode'
}

print("=" * 80)
print("MAP PAGE IDENTIFICATION")
print("=" * 80)

for city_name, folder_name in cities.items():
    city_dir = BASE_DIR / folder_name
    if not city_dir.exists():
        continue
    
    print(f"\n{'='*60}")
    print(f"City: {city_name}")
    print(f"{'='*60}")
    
    all_files = sorted(city_dir.glob('*.png'))
    
    # Categorize pages
    text_pages = []
    map_pages = []
    
    for f in all_files:
        size = f.stat().st_size
        page_num = int(f.stem.split('_')[-1])
        
        if size > MAP_SIZE_THRESHOLD:
            map_pages.append((page_num, size, f))
        else:
            text_pages.append((page_num, size, f))
    
    print(f"\n📄 Text Pages ({len(text_pages)}):")
    for page_num, size, f in text_pages:
        print(f"   Page {page_num:3d}: {size/1024:.1f} KB")
    
    print(f"\n🗺️  MAP PAGES ({len(map_pages)}):")
    for page_num, size, f in map_pages:
        print(f"   Page {page_num:3d}: {size/1024/1024:.1f} MB ★ MAP")
    
    print(f"\n✅ Recommended for georeferencing: {len(map_pages)} pages")

print(f"\n{'='*80}")
print("NEXT STEPS:")
print("=" * 80)
print("""
1. The pages marked with ★ MAP are the actual map pages
2. These are large raster images (likely scanned maps or high-res maps)
3. For each city, pick the most detailed map page (usually the largest one)

GEOREFERENCING PROCESS:
1. Open the map page in QGIS or MapWarper
2. Add 10-20 Ground Control Points (GCPs)
3. Save as GeoTIFF
4. Convert to Cloud Optimized GeoTIFF (COG)
5. Upload to Cloudflare R2
6. Update cities.json with the URL

CONTROL POINTS:
For each city, find landmarks on the map that match real-world coordinates:
- Railway stations
- Bus stands
- Major intersections
- Temples/churches
- Rivers/bridges
- Government buildings

Use Google Maps or OpenStreetMap to get the real coordinates.
""")

# Copy map pages to a separate folder for processing
MAP_PAGES_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/map-pages')
MAP_PAGES_DIR.mkdir(exist_ok=True)

for city_name, folder_name in cities.items():
    city_dir = BASE_DIR / folder_name
    output_dir = MAP_PAGES_DIR / folder_name
    output_dir.mkdir(exist_ok=True)
    
    all_files = sorted(city_dir.glob('*.png'))
    for f in all_files:
        size = f.stat().st_size
        if size > MAP_SIZE_THRESHOLD:
            # Copy to map-pages folder
            dest = output_dir / f.name
            os.system(f'cp "{f}" "{dest}"')
            print(f"✅ Copied {f.name} to {output_dir}")

print(f"\n📁 Map pages copied to: {MAP_PAGES_DIR}")
