#!/usr/bin/env python3
"""
Extract map pages from Kerala Master Plan PDFs
"""

import os
import sys
from pathlib import Path

# Try different PDF libraries
have_pymupdf = False
have_pypdf2 = True

try:
    import fitz  # PyMuPDF
    have_pymupdf = True
    print("Using PyMuPDF (fitz)")
except ImportError:
    pass

if not have_pymupdf:
    try:
        import PyPDF2
        print("Using PyPDF2")
    except ImportError:
        print("No PDF library available. Install PyMuPDF or PyPDF2.")
        sys.exit(1)

from PIL import Image

# Paths
INPUT_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/plans')
OUTPUT_DIR = Path('/Users/aadarshks/my-ai-project/kerala_map/data-processing/extracted-pages')
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_pages_with_pymupdf(pdf_path, output_dir, prefix):
    """Extract all pages as images using PyMuPDF"""
    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    print(f"PDF has {page_count} pages")
    
    extracted = []
    for i in range(page_count):
        page = doc[i]
        # Render at 300 DPI for high quality
        mat = fitz.Matrix(2, 2)  # 2x zoom for 144 DPI
        pix = page.get_pixmap(matrix=mat)
        
        output_path = output_dir / f"{prefix}_page_{i+1:03d}.png"
        pix.save(str(output_path))
        extracted.append(output_path)
        
        if i % 10 == 0:
            print(f"  Extracted page {i+1}/{page_count}")
    
    doc.close()
    return extracted

def extract_pages_with_pypdf2(pdf_path, output_dir, prefix):
    """Extract text and page info using PyPDF2"""
    reader = PyPDF2.PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    print(f"PDF has {page_count} pages")
    
    # Extract text from first few pages to understand structure
    for i in range(min(5, page_count)):
        text = reader.pages[i].extract_text()
        print(f"\nPage {i+1} preview:")
        print(text[:500] if text else "No text (likely image/map)")
    
    return page_count

def analyze_pdf(city_name, pdf_filename):
    pdf_path = INPUT_DIR / pdf_filename
    print(f"\n{'='*60}")
    print(f"Analyzing: {city_name}")
    print(f"File: {pdf_filename}")
    print(f"Size: {pdf_path.stat().st_size / (1024*1024):.1f} MB")
    print(f"{'='*60}")
    
    city_output_dir = OUTPUT_DIR / city_name.lower().replace(' ', '-')
    city_output_dir.mkdir(exist_ok=True)
    
    if have_pymupdf:
        extracted = extract_pages_with_pymupdf(pdf_path, city_output_dir, city_name.lower().replace(' ', '_'))
        print(f"Extracted {len(extracted)} pages")
        return extracted
    else:
        page_count = extract_pages_with_pypdf2(pdf_path, city_output_dir, city_name.lower().replace(' ', '_'))
        return page_count

# Process all 3 cities
cities = [
    ("Thiruvananthapuram", "trivandrum-master-plan.pdf"),
    ("Kochi", "kochi-master-plan.pdf"),
    ("Kozhikode", "kozhikode-master-plan.pdf")
]

all_extracted = {}
for city, pdf in cities:
    try:
        result = analyze_pdf(city, pdf)
        all_extracted[city] = result
    except Exception as e:
        print(f"ERROR processing {city}: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print("Extraction complete!")
print(f"Output directory: {OUTPUT_DIR}")
print(f"{'='*60}")

# List extracted files
for city in cities:
    city_dir = OUTPUT_DIR / city[0].lower().replace(' ', '-')
    if city_dir.exists():
        files = sorted(city_dir.glob('*.png'))
        print(f"\n{city[0]}: {len(files)} pages extracted")
        print(f"  Location: {city_dir}")
        if files:
            print(f"  Sample: {files[0].name}")
            # Get image dimensions
            img = Image.open(files[0])
            print(f"  Resolution: {img.size[0]}x{img.size[1]} pixels")
