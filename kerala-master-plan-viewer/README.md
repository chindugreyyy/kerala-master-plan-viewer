# Kerala Master Plan Viewer

A web application for viewing georeferenced development plans (master plans) of all cities and towns in Kerala. Built for **Kerala First** (keralafirst.co.in).

## Features

- **All 43 Kerala cities & towns** — Corporations, municipalities, and major towns
- **City selector** — Searchable dropdown with data availability indicators
- **Address search** — Find any place in Kerala using OpenStreetMap Nominatim
- **Geolocation** — Navigate to your current location
- **Opacity slider** — Adjust overlay transparency
- **Swipe compare** — Draggable divider to compare plan vs. basemap
- **Basemap toggle** — Switch between street map and satellite imagery
- **Dark mode** — Toggle between light and dark themes
- **Comments system** — Add location-based comments on plans (requires Supabase)
- **Mobile responsive** — Works on phones, tablets, and desktops
- **India boundary compliance** — Uses corrected boundary tiles for India

## Project Structure

```
├── index.html       — HTML shell with CDN imports
├── main.js          — All application logic (map, controls, COG loading)
├── style.css        — Styling with CSS variables for theming
├── cities.json      — Kerala cities with coordinates (43 cities/towns)
├── README.md        — This file
└── DATA_GUIDE.md    — How to add master plan data
```

## Quick Start

1. Serve with any local HTTP server:

```bash
# Python
python -m http.server 8000

# Node
npx serve .
```

2. Open `http://localhost:8000`

3. Select a city from the dropdown to navigate to it

## Deploying to keralafirst.co.in

### Option 1: WordPress Page (Recommended)

1. Upload the project files to your WordPress server via FTP or File Manager:
   - Create a folder: `/public_html/master-plan-viewer/`
   - Upload all files (`index.html`, `main.js`, `style.css`, `cities.json`)

2. Create a WordPress page with a Custom HTML block:
```html
<iframe src="https://keralafirst.co.in/master-plan-viewer/" 
        width="100%" height="800px" 
        frameborder="0" 
        style="border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
</iframe>
```

3. Or create a direct link in your navigation menu to the viewer.

### Option 2: Subdomain

1. Create a subdomain in cPanel: `maps.keralafirst.co.in`
2. Point it to the uploaded folder
3. Access directly at `https://maps.keralafirst.co.in`

### Option 3: GitHub Pages

1. Push this code to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Use a custom domain: `maps.keralafirst.co.in` (or similar)
4. Add a CNAME record in your DNS pointing to GitHub Pages

## Adding Master Plan Data

See [DATA_GUIDE.md](DATA_GUIDE.md) for detailed instructions on:
- Finding Kerala master plans
- Georeferencing scanned PDFs
- Converting to Cloud Optimized GeoTIFFs
- Uploading to cloud storage
- Updating cities.json

## Setting Up Comments (Supabase)

The comments system requires a Supabase backend. To set up your own:

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Create a table called `suggestions` with columns:
   - `id` (bigint, auto-increment, primary key)
   - `created_at` (timestamp, default now())
   - `city` (text, not null)
   - `lng` (float8, not null)
   - `lat` (float8, not null)
   - `type` (text, default 'suggestion')
   - `category` (text, default 'other')
   - `text` (text, not null)
   - `author_name` (text, nullable)
4. Enable Row Level Security (RLS) and allow anonymous inserts
5. Copy your Supabase URL and anon key into `main.js`

## Technical Details

- **Mapping**: OpenLayers 10.9.0 with WebGLTile rendering
- **Projection**: EPSG:3857 (Web Mercator)
- **Data formats**: Cloud Optimized GeoTIFFs (COG) or XYZ tiles
- **Basemaps**: OpenStreetMap (India corrected) + Esri World Imagery
- **Geocoding**: Nominatim (OpenStreetMap)
- **Backend**: Supabase (PostgreSQL)
- **No build step required**

## Browser Support

Any modern browser with WebGL2 support (Chrome, Firefox, Edge, Safari 16.4+).

## Credits

- Based on the open-source [Master Plan Viewer](https://github.com/datsvarun/master-plan-viewer) by Varun
- Adapted for Kerala by Kerala First
- Kerala State Town Planning Department for plan data

## License

MIT License — feel free to use and modify.

## Contact

For adding master plan data or reporting issues:
- Website: [keralafirst.co.in](https://keralafirst.co.in)
- Email: (your contact email)
