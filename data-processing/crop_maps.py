#!/usr/bin/env python3
"""
Better cropping - detect actual map content area
"""

from PIL import Image
import numpy as np
from pathlib import Path

def analyze_and_crop(city_name, input_file, output_file):
    img = Image.open(input_file)
    arr = np.array(img)
    
    # Convert to grayscale
    if len(arr.shape) == 3:
        gray = np.mean(arr, axis=2)
    else:
        gray = arr
    
    # Detect rows with significant content (not just white)
    # A row has content if > 20% of pixels are non-white (< 240)
    threshold = 240
    row_content_ratio = np.mean(gray < threshold, axis=1)
    col_content_ratio = np.mean(gray < threshold, axis=0)
    
    # Find rows/cols with > 20% content
    content_rows = np.where(row_content_ratio > 0.2)[0]
    content_cols = np.where(col_content_ratio > 0.2)[0]
    
    if len(content_rows) == 0 or len(content_cols) == 0:
        print(f"{city_name}: No clear content found")
        return None
    
    top = content_rows[0]
    bottom = content_rows[-1]
    left = content_cols[0]
    right = content_cols[-1]
    
    # Add padding
    padding = 20
    top = max(0, top - padding)
    bottom = min(gray.shape[0], bottom + padding)
    left = max(0, left - padding)
    right = min(gray.shape[1], right + padding)
    
    print(f"\n{city_name}:")
    print(f"  Original: {img.size}")
    print(f"  Content area: ({left}, {top}, {right}, {bottom})")
    print(f"  Cropped: {right-left} x {bottom-top}")
    print(f"  Removed: {img.size[0] - (right-left)}px horizontal, {img.size[1] - (bottom-top)}px vertical")
    
    # Crop
    cropped = img.crop((left, top, right, bottom))
    cropped.save(output_file, 'PNG')
    
    return (left, top, right, bottom)

# Process all 3 cities
BASE_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/map-pages')
OUTPUT_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/cropped')
OUTPUT_DIR.mkdir(exist_ok=True)

cities = {
    'thiruvananthapuram': 'thiruvananthapuram/thiruvananthapuram_page_008.png',
    'kochi': 'kochi/kochi_page_008.png',
    'kozhikode': 'kozhikode/kozhikode_page_009.png'
}

for city, path in cities.items():
    input_file = BASE_DIR / path
    output_file = OUTPUT_DIR / f"{city}_cropped.png"
    analyze_and_crop(city, input_file, output_file)

print(f"\n✅ Cropped images saved to: {OUTPUT_DIR}")
