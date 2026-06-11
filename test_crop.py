#!/usr/bin/env python3
"""
Better cropping using brightness profile analysis
"""

from PIL import Image
import numpy as np
from pathlib import Path

# Test on Kochi
img = Image.open('/Users/aadarshks/my-ai-project/kerala_map/data-processing/map-pages/kochi/kochi_page_008.png')
arr = np.array(img)

# Convert to grayscale
gray = np.mean(arr, axis=2)

# Analyze row by row - find where content starts
row_means = np.mean(gray, axis=1)
row_mins = np.min(gray, axis=1)
row_maxs = np.max(gray, axis=1)

# Find rows where content exists (min < 200 or max < 240)
# Content should have some darker pixels
content_rows = np.where((row_mins < 200) | (row_maxs < 240))[0]

# Analyze column by column
col_means = np.mean(gray, axis=0)
col_mins = np.min(gray, axis=0)
col_maxs = np.max(gray, axis=0)

content_cols = np.where((col_mins < 200) | (col_maxs < 240))[0]

print(f"Image shape: {gray.shape}")
print(f"Content rows: {content_rows[0]} to {content_rows[-1]} (count: {len(content_rows)})")
print(f"Content cols: {content_cols[0]} to {content_cols[-1]} (count: {len(content_cols)})")
print(f"Suggested crop: ({content_cols[0]}, {content_rows[0]}, {content_cols[-1]}, {content_rows[-1]})")
print(f"Crop size: {content_cols[-1] - content_cols[0]} x {content_rows[-1] - content_rows[0]}")
print(f"Original size: {img.size}")

# Check if there's significant margin
print(f"\nTop margin: {content_rows[0]} pixels")
print(f"Bottom margin: {gray.shape[0] - content_rows[-1]} pixels")
print(f"Left margin: {content_cols[0]} pixels")
print(f"Right margin: {gray.shape[1] - content_cols[-1]} pixels")

# Show sample of edge vs content
print(f"\nRow 50 (top edge): min={row_mins[50]:.1f}, max={row_maxs[50]:.1f}, mean={row_means[50]:.1f}")
print(f"Row 500 (maybe content): min={row_mins[500]:.1f}, max={row_maxs[500]:.1f}, mean={row_means[500]:.1f}")
print(f"Row 3000 (center): min={row_mins[3000]:.1f}, max={row_maxs[3000]:.1f}, mean={row_means[3000]:.1f}")
print(f"Row 8000 (bottom): min={row_mins[8000]:.1f}, max={row_maxs[8000]:.1f}, mean={row_means[8000]:.1f}")
