# Kerala Master Plan Georeferencing Guide

## Overview

This guide explains how to convert the extracted PDF map pages into georeferenced Cloud Optimized GeoTIFFs (COGs) that can be used in the Kerala Master Plan Viewer.

## Map Pages Identified

### Thiruvananthapuram
- **Pages 8, 9, 10** (31.4 MB, 26.0 MB, 18.8 MB)
- **Best candidate:** Page 008 (largest, most detailed)
- **Location:** `data-processing/map-pages/thiruvananthapuram/thiruvananthapuram_page_008.png`

### Kochi
- **Pages 7, 8, 9** (43.9 MB, 44.1 MB, 27.0 MB)
- **Best candidate:** Page 008 (largest, most detailed)
- **Location:** `data-processing/map-pages/kochi/kochi_page_008.png`

### Kozhikode
- **Pages 8, 9, 10** (38.4 MB, 44.2 MB, 36.3 MB)
- **Best candidate:** Page 009 (largest, most detailed)
- **Location:** `data-processing/map-pages/kozhikode/kozhikode_page_009.png`

## Method 1: MapWarper (Recommended for beginners)

### Step 1: Upload to MapWarper
1. Go to https://mapwarper.net/
2. Create a free account
3. Click "Upload Map"
4. Upload the PNG file (e.g., `thiruvananthapuram_page_008.png`)
5. Fill in metadata:
   - Title: "Thiruvananthapuram Master Plan 2021"
   - Description: "Kerala LSGD Official Master Plan"
   - Tags: "kerala, master-plan, thiruvananthapuram"

### Step 2: Add Control Points
1. Click "Rectify" tab
2. Find at least 10-15 identifiable landmarks on both the map and the base map
3. Good landmarks:
   - Railway stations (Thiruvananthapuram Central, Ernakulam Junction, Kozhikode)
   - Major bus stands
   - Temples (Padmanabhaswamy Temple, Guruvayur)
   - Major bridges
   - Government buildings (Secretariat, Collectorate)
   - Major intersections

### Step 3: Warp and Export
1. Click "Warp Image" with transformation method "Polynomial" or "Thin Plate Spline"
2. Download the resulting GeoTIFF
3. The file will have embedded georeferencing information

### Step 4: Convert to COG
```bash
# Using GDAL (install with: brew install gdal)
gdal_translate \
  -of COG \
  -co COMPRESS=DEFLATE \
  -co RESAMPLING=AVERAGE \
  -co OVERVIEW_RESAMPLING=AVERAGE \
  -co BLOCKSIZE=512 \
  input.tif \
  output_cog.tif
```

## Method 2: QGIS (More control)

### Step 1: Install QGIS
```bash
brew install qgis
```

### Step 2: Open the Map
1. Open QGIS
2. Drag the PNG file into the project
3. It will ask for CRS - select "Undefined" (we'll georeference it)

### Step 3: Georeference
1. Go to Raster → Georeferencer
2. Open the PNG file
3. Add control points (GCPs):
   - Click on a point on the map image
   - Enter the real-world coordinates (from Google Maps or OSM)
   - Add at least 10-15 points spread across the entire map
4. Set transformation: Polynomial 2 (or 3)
5. Set output CRS: EPSG:4326 (WGS 84)
6. Run and save as GeoTIFF

### Step 4: Convert to COG
```bash
gdal_translate -of COG -co COMPRESS=DEFLATE input.tif output_cog.tif
```

## Control Points (Sample)

### Thiruvananthapuram
| Landmark | Latitude | Longitude |
|----------|----------|-----------|
| Thiruvananthapuram Central Railway Station | 8.4875 | 76.9525 |
| Padmanabhaswamy Temple | 8.4828 | 76.9436 |
| Kerala Secretariat | 8.5058 | 76.9492 |
| Napier Museum | 8.5083 | 76.9561 |
| Vellayani Lake | 8.4019 | 77.0292 |
| Kovalam Beach | 8.4009 | 76.9784 |
| Technopark | 8.5571 | 76.8816 |
| Kazhakootam | 8.5472 | 76.8733 |
| Attukal Temple | 8.4681 | 76.9478 |
| Sree Chitra Art Gallery | 8.5083 | 76.9558 |

### Kochi
| Landmark | Latitude | Longitude |
|----------|----------|-----------|
| Ernakulam Junction Railway Station | 9.9836 | 76.2828 |
| Fort Kochi | 9.9667 | 76.2425 |
| Marine Drive | 9.9831 | 76.2781 |
| Lulu Mall | 10.0269 | 76.3075 |
| Infopark | 10.0097 | 76.3631 |
| Cochin International Airport | 10.1520 | 76.4019 |
| Hill Palace Museum | 9.9586 | 76.3631 |
| Cherai Beach | 10.1425 | 76.1786 |
| Bolgatty Palace | 9.9917 | 76.2681 |
| Edappally Church | 10.0264 | 76.3081 |

### Kozhikode
| Landmark | Latitude | Longitude |
|----------|----------|-----------|
| Kozhikode Railway Station | 11.2486 | 75.7808 |
| Mananchira Square | 11.2586 | 75.7811 |
| Kozhikode Beach | 11.2575 | 75.7708 |
| Kappad Beach | 11.3881 | 75.6925 |
| Calicut University | 11.1381 | 75.8958 |
| Medical College | 11.2781 | 75.8408 |
| Beypore Port | 11.1758 | 75.8058 |
| Kakkayam | 11.4583 | 75.8783 |
| Thusharagiri Falls | 11.4833 | 75.8833 |
| IIM Kozhikode | 11.3519 | 75.8364 |

## Cloudflare R2 Upload

After creating the COG files:

1. Create R2 bucket: `kerala-master-plans`
2. Upload files:
```bash
# Using rclone or aws CLI
aws s3 cp thiruvananthapuram_cog.tif s3://kerala-master-plans/
aws s3 cp kochi_cog.tif s3://kerala-master-plans/
aws s3 cp kozhikode_cog.tif s3://kerala-master-plans/
```
3. Make files public with custom domain: `https://plans.keralafirst.co.in/`

## COG Specifications

- **Format:** Cloud Optimized GeoTIFF (COG)
- **CRS:** EPSG:4326 (WGS 84)
- **Compression:** DEFLATE
- **Block Size:** 512x512
- **Overviews:** Generated automatically
- **Color:** RGBA (if map has colors) or RGB

## Expected File Sizes

After COG conversion:
- Thiruvananthapuram: ~25-30 MB
- Kochi: ~35-40 MB
- Kozhikode: ~35-40 MB

## Testing

After uploading, test with:
```bash
curl -I https://plans.keralafirst.co.in/thiruvananthapuram_cog.tif
```

Check headers include:
- `Content-Type: image/tiff`
- `Accept-Ranges: bytes`

## Viewer Integration

Update `cities.json`:
```json
{
  "name": "Thiruvananthapuram",
  "cogUrl": "https://plans.keralafirst.co.in/thiruvananthapuram_cog.tif",
  "dataSource": "official",
  "dataSourceUrl": "https://lsgd.kerala.gov.in/..."
}
```

## Troubleshooting

### Map is not aligned
- Add more control points (minimum 10)
- Use points spread across corners and edges
- Try different transformation (Polynomial 2 vs 3)

### File too large
- Reduce resolution during export: `gdal_translate -outsize 50% 50%`
- Use JPEG compression: `gdal_translate -co COMPRESS=JPEG -co QUALITY=85`

### Colors look wrong
- Check if PNG has transparency (alpha channel)
- Use `-co ALPHA=YES` if needed

## Progress Tracking

| City | Status | Map Page | Control Points | COG Created | Uploaded |
|------|--------|----------|---------------|-------------|----------|
| Thiruvananthapuram | ⏳ Pending | 008 | 0/15 | No | No |
| Kochi | ⏳ Pending | 008 | 0/15 | No | No |
| Kozhikode | ⏳ Pending | 009 | 0/15 | No | No |

## Next Steps

1. ✅ Download PDFs
2. ✅ Extract pages
3. ✅ Identify map pages
4. 🔄 Georeference maps (MANUAL - requires landmarks)
5. ⏳ Convert to COG
6. ⏳ Upload to R2
7. ⏳ Update viewer
8. ⏳ Deploy

## Notes

- The map pages are large PNGs (1190x1684 pixels at 144 DPI)
- Resolution may be insufficient for detailed street-level analysis
- Consider downloading the original PDF at full resolution if needed
- For higher accuracy, use more control points (20-30)
- The proxy layer (OSM data) provides fallback for areas outside the map
