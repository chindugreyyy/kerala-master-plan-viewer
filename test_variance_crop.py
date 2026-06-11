#!/usr/bin/env python3
"""
Aggressive cropping - find actual map content by looking for variance
"""

from PIL import Image
import numpy as np
from pathlib import Path

def find_map_bounds(city_name, input_file):
    """Find the actual map content area by looking for variance"""
    img = Image.open(input_file)
    arr = np.array(img)
    
    # Convert to grayscale
    if len(arr.shape) == 3:
        gray = np.mean(arr, axis=2)
    else:
        gray = arr
    
    # Calculate variance in small windows to find content
    window_size = 50
    
    # Check rows: find where there's significant variance
    row_vars = []
    for i in range(0, gray.shape[0], window_size):
        end = min(i + window_size, gray.shape[0])
        window = gray[i:end]
        row_vars.append(np.var(window))
    
    # Check columns
    col_vars = []
    for j in range(0, gray.shape[1], window_size):
        end = min(j + window_size, gray.shape[1])
        window = gray[:, j:end]
        col_vars.append(np.var(window))
    
    # Find content windows (variance > threshold)
    var_threshold = 100  # Adjust based on content
    content_row_indices = np.where(np.array(row_vars) > var_threshold)[0]
    content_col_indices = np.where(np.array(col_vars) > var_threshold)[0]
    
    if len(content_row_indices) == 0 or len(content_col_indices) == 0:
        print(f"{city_name}: No content found with threshold {var_threshold}")
        return None
    
    # Convert window indices back to pixel coordinates
    top = content_row_indices[0] * window_size
    bottom = min((content_row_indices[-1] + 1) * window_size, gray.shape[0])
    left = content_col_indices[0] * window_size
    right = min((content_col_indices[-1] + 1) * window_size, gray.shape[1])
    
    print(f"\n{city_name}:")
    print(f"  Original: {img.size}")
    print(f"  Content bounds: ({left}, {top}, {right}, {bottom})")
    print(f"  Cropped: {right-left} x {bottom-top}")
    
    return (left, top, right, bottom)

# Test with Kochi
BASE_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/map-pages')

for city, path in [
    ('kochi', 'kochi/kochi_page_008.png'),
    ('thiruvananthapuram', 'thiruvananthapuram/thiruvananthapuram_page_008.png'),
    ('kozhikode', 'kozhikode/kozhikode_page_009.png')
]:
    input_file = BASE_DIR / path
    find_map_bounds(city, input_file)
