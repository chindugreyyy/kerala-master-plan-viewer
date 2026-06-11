# Kerala Master Plan Data Guide

This guide explains how to add georeferenced master plan data for Kerala cities and towns to the viewer.

## Understanding the Data

### What You Need

For each city/town, you need either:

1. **Cloud Optimized GeoTIFF (COG)** — Recommended
   - A georeferenced TIFF file optimized for web streaming
   - Hosted on a cloud storage with CORS enabled (Cloudflare R2, AWS S3, Google Cloud)
   - Added as `cogUrl` in `cities.json`

2. **XYZ Tiles**
   - Pre-rendered map tiles (like Google Maps tiles)
   - Hosted on a tile server (MapWarper, Mapbox, etc.)
   - Added as `xyzUrl` in `cities.json`

### What You Have (Usually)

Government master plans are typically:
- PDF documents (scanned images)
- CAD drawings (DXF/DWG)
- Paper maps

These need to be **georeferenced** before they can be displayed on the web map.

---

## Step 1: Find Kerala Master Plans

### Official Sources

1. **Kerala State Town Planning Department**
   - Website: [tsp.kerala.gov.in](https://tsp.kerala.gov.in) (check current URL)
   - May have development plans for municipalities

2. **Kerala State Spatial Data Infrastructure (KSDI)**
   - Kerala GIS portal
   - May have downloadable geospatial data

3. **Individual Municipal Corporation Websites**
   - Thiruvananthapuram Corporation
   - Kochi Corporation
   - Kozhikode Corporation
   - Kollam Corporation
   - Thrissur Corporation
   - Kannur Corporation

4. **Kerala Town & Country Planning Department**
   - District planning offices
   - Physical plan documents

5. **RTI (Right to Information)**
   - If plans are not publicly available, file RTI requests

### Alternative Sources

- **Google search**: "{city name} master plan PDF" or "{city name} development plan"
- **Research papers**: Academics may have georeferenced data
- **Urban planning institutes**: NITs, IITs, etc.

---

## Step 2: Georeference the Plan

Georeferencing means assigning real-world coordinates (latitude/longitude) to points on the scanned map.

### Method A: Using MapWarper (Easiest, Free)

**MapWarper** is a web tool that lets you georeference maps and serves them as XYZ tiles.

1. Go to [mapwarper.net](https://mapwarper.net)
2. Create an account
3. Click "Upload Map"
4. Upload your scanned PDF/image of the master plan
5. Add control points:
   - Find recognizable landmarks on the scanned map (road intersections, buildings, rivers)
   - Click on the map image, then find the same location on the base map
   - Add at least 6-10 points for accuracy
6. Click "Rectify" to process
7. Click "Export" → "Tiles" to get the XYZ URL
8. The URL will look like: `https://mapwarper.net/maps/tile/{id}/{z}/{x}/{y}.png`
9. Add this as `xyzUrl` in `cities.json`

**Pros**: Free, no software needed, automatic tile serving
**Cons**: Limited customization, depends on external service

### Method B: Using QGIS (More Control, Free)

**QGIS** is a free desktop GIS software.

1. Download and install [QGIS](https://qgis.org)
2. Open QGIS
3. Go to **Raster → Georeferencer**
4. Open your scanned image/PDF
5. Add Ground Control Points (GCPs):
   - Click on a known point in the image
   - Enter the real-world coordinates (you can get these from Google Maps or OpenStreetMap)
   - Repeat for at least 6-10 points spread across the map
6. Choose transformation type: **Polynomial 2** or **Thin Plate Spline**
7. Set target CRS to **EPSG:4326** (WGS 84)
8. Click "Start Georeferencing"
9. Save as `georeferenced_plan.tif`

**Pros**: More accurate, works offline, full control
**Cons**: Requires learning QGIS, manual process

### Method C: Using Google Earth Pro (Simple)

1. Download [Google Earth Pro](https://www.google.com/earth/versions/) (free)
2. Open your scanned image as an overlay
3. Adjust transparency and position
4. Add landmarks to align the image
5. Export the image (it will be georeferenced)

**Pros**: Very visual, easy to use
**Cons**: Less precise than QGIS

---

## Step 3: Convert to Cloud Optimized GeoTIFF (COG)

If you used QGIS or have a regular GeoTIFF, convert it to COG for web use.

### Using GDAL (Command Line)

```bash
# Install GDAL first (brew install gdal on Mac, apt-get install gdal-bin on Linux)

# Convert to COG with WEBP compression
gdal_translate \
  -of COG \
  -co COMPRESS=WEBP \
  -co QUALITY=80 \
  -co OVERVIEW_RESAMPLING=BILINEAR \
  input.tif \
  output_cog.tif

# Or with LZW compression (more compatible)
gdal_translate \
  -of COG \
  -co COMPRESS=LZW \
  -co OVERVIEW_RESAMPLING=BILINEAR \
  input.tif \
  output_cog.tif
```

### Using Python

```python
from osgeo import gdal

input_file = "input.tif"
output_file = "output_cog.tif"

# Open input
src = gdal.Open(input_file)

# Create copy as COG
options = gdal.TranslateOptions(
    format='COG',
    creationOptions=['COMPRESS=WEBP', 'QUALITY=80']
)
gdal.Translate(output_file, src, options=options)
```

### Using QGIS

1. Open the georeferenced raster in QGIS
2. Right-click → Export → Save As
3. Format: "COG" (Cloud Optimized GeoTIFF)
4. Compression: WEBP or LZW
5. Click OK

---

## Step 4: Upload to Cloud Storage

The COG file needs to be hosted on a server with **CORS enabled** so the browser can access it.

### Option 1: Cloudflare R2 (Recommended)

1. Create a Cloudflare account
2. Go to R2 in the dashboard
3. Create a bucket: `kerala-master-plans`
4. Upload your `.tif` files
5. Enable CORS:
   ```json
   {
     "AllowedOrigins": ["https://keralafirst.co.in", "http://localhost:*"],
     "AllowedMethods": ["GET", "HEAD"],
     "AllowedHeaders": ["*"],
     "MaxAgeSeconds": 3600
   }
   ```
6. Get the public URL: `https://pub-xxxxx.r2.dev/City-Tiles/filename.tif`
7. Add this as `cogUrl` in `cities.json`

### Option 2: AWS S3

1. Create an S3 bucket
2. Upload files
3. Enable public access and CORS
4. Use S3 static website URL or CloudFront CDN

### Option 3: Google Cloud Storage

1. Create a bucket
2. Upload files
3. Set public permissions
4. Configure CORS

### Option 4: GitHub (For Small Files)

1. Upload files to a GitHub repository
2. Use GitHub raw URLs
3. **Note**: GitHub has file size limits and rate limits

---

## Step 5: Update cities.json

For each city that now has data, update the `cities.json` file:

```json
{
  "name": "Thiruvananthapuram",
  "cogUrl": "https://pub-xxxxx.r2.dev/City-Tiles/Thiruvananthapuram_DP.tif",
  "center": [76.9366, 8.5241],
  "zoom": 12
}
```

Or for XYZ tiles:
```json
{
  "name": "Kochi",
  "xyzUrl": "https://mapwarper.net/maps/tile/12345/{z}/{x}/{y}.png",
  "center": [76.2673, 9.9312],
  "zoom": 12
}
```

### Coordinates

- `center`: [longitude, latitude] — use Google Maps or OpenStreetMap to find
- `zoom`: Zoom level (10 for regions, 12 for cities, 13 for towns)

### Getting Coordinates

1. Go to [Google Maps](https://maps.google.com)
2. Right-click on the city center
3. Copy the coordinates (lat, lng)
4. In `cities.json`, use [lng, lat] format (reverse!)

---

## Step 6: Test and Verify

1. Save `cities.json`
2. Refresh the viewer in your browser
3. Select the city from dropdown
4. Verify the overlay appears correctly
5. Check that the overlay aligns with the basemap
6. If misaligned, go back and add more control points in the georeferencing step

---

## Tips for Accuracy

1. **Use many control points** — 10-20 is better than 4-5
2. **Spread points across the map** — Don't cluster them in one corner
3. **Use precise landmarks** — Road intersections, building corners, bridges
4. **Check multiple locations** — Verify accuracy in different parts of the map
5. **Use high-resolution scans** — Higher DPI = better accuracy
6. **Match the projection** — Kerala plans may use a local projection; convert to WGS84

---

## Common Issues

### Issue: CORS Errors

**Error**: `Access-Control-Allow-Origin` header missing

**Solution**: Enable CORS on your cloud storage bucket. See Step 4.

### Issue: Tiles Not Loading

**Error**: Blank overlay or broken tiles

**Solutions**:
- Check the URL is correct and publicly accessible
- Verify the file is a valid COG: `gdalinfo filename.tif` should show `LAYOUT=COG`
- Check browser console for specific errors

### Issue: Misaligned Overlay

**Error**: Plan doesn't match roads/buildings on basemap

**Solutions**:
- Add more control points
- Use higher-order transformation (Polynomial 2 instead of 1)
- Check that coordinates are in correct CRS
- Re-scan at higher resolution

### Issue: File Too Large

**Error**: Slow loading or browser crashes

**Solutions**:
- Use WEBP compression (smaller than JPEG/TIFF)
- Reduce resolution if not needed
- Use overview pyramids (built into COG format)
- Consider tiling instead of COG

---

## Current Kerala Data Status

| City | Status | Source | Notes |
|------|--------|--------|-------|
| Thiruvananthapuram | 🔴 No data | Need to source | Corporation plan available? |
| Kochi | 🔴 No data | Need to source | GCDA plan? |
| Kozhikode | 🔴 No data | Need to source | Corporation plan? |
| ... | ... | ... | ... |

**Help wanted!** If you have access to Kerala master plans, please contribute them.

---

## Resources

- [OpenLayers GeoTIFF Documentation](https://openlayers.org/workshop/en/cog/)
- [MapWarper Tutorial](https://mapwarper.net/)
- [QGIS Georeferencing Tutorial](https://docs.qgis.org/3.28/en/docs/user_manual/working_with_raster/georeferencer.html)
- [GDAL COG Documentation](https://gdal.org/drivers/raster/cog.html)
- [Cloudflare R2 CORS Guide](https://developers.cloudflare.com/r2/buckets/cors/)

---

## Contact for Data Contributions

If you have Kerala master plans (PDFs, scans, or digital files) and want to help add them to the viewer:

1. Email them to: (your email)
2. Or upload to: (your upload link)
3. Or contact via: (your contact form)

We can help georeference and convert them for web use.
