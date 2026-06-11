# Publicly Available Data Sources for Kerala Cities
## Thiruvananthapuram (Trivandrum), Kochi (Ernakulam), and Kozhikode (Calicut)

---

## 1. KERALA STATE SPATIAL DATA INFRASTRUCTURE (KSDI)

**Status:** Portal exists but was inaccessible during research (connection timeouts).

**Known Information:**
- KSDI was established as part of the National Spatial Data Infrastructure (NSDI) initiative
- It is meant to provide geospatial data layers for Kerala including:
  - Land use/land cover maps
  - Cadastral data (village maps, field boundary data)
  - Road networks
  - Drainage/water bodies
  - Administrative boundaries
  - Topographic data

**Attempted URLs:**
- `https://ksdi.kerala.gov.in` (Transport error)
- `https://gis.kerala.gov.in` (Transport error)
- `https://geoportal.kerala.gov.in` (Transport error)

**Alternative Access:**
- Contact: Kerala State Remote Sensing and Environment Centre (KSRSEC)
- Through Kerala State Planning Board's GIS cell
- The Town Planning Department may have KSDI-derived maps

---

## 2. BHUVAN KERALA (ISRO)

**Status:** Main Bhuvan portal accessible; Kerala-specific data available through national portal.

**Available Data:**
Bhuvan (https://bhuvan.nrsc.gov.in) provides:
- High-resolution satellite imagery (Cartosat, Resourcesat)
- Land use/land cover maps (National level, scale 1:50,000)
- Urban sprawl mapping
- Coastal zone maps
- Disaster management layers
- Open Series Maps (OSM) from Survey of India

**Specific Kerala Data:**
- Bhuvan has state-level thematic maps including Kerala
- Land Use/Land Cover maps for all districts
- Urban area boundaries
- Road network data
- Drainage patterns
- Vegetation indices

**Data Download:**
- Bhuvan provides data download through Bhuvan Geo-Portal
- Requires registration
- Data formats: Shapefiles, KML, GeoTIFF
- URL: `https://bhuvan.nrsc.gov.in`

**Important Note:** Many Bhuvan sub-portals require Java or specific plugins. The main portal is being modernized.

---

## 3. KERALA TOWN PLANNING DEPARTMENT / LOCAL SELF GOVERNMENT DEPARTMENT (LSGD)

**Status:** MAJOR FIND - Direct PDF master plans available for all 3 cities!

**Direct PDF Links (Confirmed Working):**

### Thiruvananthapuram City Master Plan:
- **URL:** https://lsgd.kerala.gov.in/wp-content/uploads/2025/08/Thiruvananthapuram-City-Master-Plan.pdf
- **Source:** LSGD Kerala Official Website
- **Type:** PDF (Master Plan)

### Kochi City Master Plan:
- **URL:** https://lsgd.kerala.gov.in/wp-content/uploads/2025/08/Kochi-City-Master-Plan.pdf
- **Source:** LSGD Kerala Official Website
- **Type:** PDF (Master Plan)

### Kozhikode City Master Plan:
- **URL:** https://lsgd.kerala.gov.in/wp-content/uploads/2025/08/Kozhikode-Master-Plan.pdf
- **Source:** LSGD Kerala Official Website
- **Type:** PDF (Master Plan)

**All Master Plans Index:**
- **URL:** https://lsgd.kerala.gov.in/en/regulations-and-policies/masterplans/
- Cities covered: Thiruvananthapuram, Kochi, Kozhikode, Kollam, Alappuzha, Thrissur, Palakkad, Kannur, Guruvayur

**Additional Documents from LSGD:**
- Kerala Panchayat Raj Act
- Kerala Municipal Raj Act
- Town and Country Planning Act
- Kerala Municipal Building Rules
- Kerala Panchayat Building Rules
- **URL:** https://lsgd.kerala.gov.in/en/regulations-and-policies/policies-acts-and-rules/

**Kudumbashree (LSGD-linked) GIS Data:**
- Enterprise location maps
- Snehitha center locations
- DDU-GKY training center maps
- Nano market locations
- **URL:** https://www.kudumbashree.org/pages/550

---

## 4. SMART CITY MISSION

**Status:** All three cities are Smart Cities under India's Smart Cities Mission.

**Confirmed Smart Cities:**
- Thiruvananthapuram (Selected in Round 1)
- Kochi (Selected in Round 1)
- Kozhikode (Selected in Round 2)

**Official Portal:**
- National Smart Cities Portal: `https://smartcities.gov.in` (Transport error during research)
- The portal contains:
  - Smart City Proposals (SCP) for each city
  - Detailed Project Reports (DPRs)
  - Area-based development plans
  - Pan-city solutions
  - Tender documents
  - Progress reports

**City-specific Data:**
- Each city corporation has Smart City cells
- **Kochi:** Kochi Smart City initiatives include water metro, intelligent transport
- **Thiruvananthapuram:** Focus on IT zone, heritage conservation, water bodies
- **Kozhikode:** Focus on beach development, heritage, commercial areas

**Kerala Impact Portal (LSGD):**
- https://impactkerala.lsgkerala.gov.in/en/
- Contains progress of various urban development projects

---

## 5. GOOGLE EARTH / GOOGLE MAPS

**Google Earth Engine:**
- **URL:** https://earthengine.google.com
- **Data:** 37+ years of historical satellite imagery
- **Access:** Free for research, education, and non-commercial use
- **API:** Python and JavaScript APIs available
- **Datasets:** Landsat (1972-present), Sentinel-2 (2015-present), MODIS, etc.

**Google Earth Pro (Desktop):**
- Free download
- Historical imagery viewer (back to ~1984 for many areas)
- Can save images and export KMZ

**Google Maps Platform:**
- Street View available for all 3 cities
- Maps API for custom applications
- Static maps API

**Google Earth Timelapse:**
- **URL:** https://g.co/timelapse
- Visualize urban growth from 1984 to 2020

**Data Extraction Methods:**
- Earth Engine Code Editor: `https://code.earthengine.google.com`
- Sample code for Kerala bounding box extraction available
- Satellite imagery can be downloaded in GeoTIFF format

---

## 6. OPENSTREETMAP (OSM)

**Data Availability:**
- Comprehensive coverage for all 3 cities
- Regularly updated by local mappers
- Kerala has an active OSM community

**Data Layers Tagged:**
- Buildings (building=yes, building types)
- Roads (highway=*, surface, lanes)
- Land use (landuse=residential, commercial, industrial, forest, etc.)
- Amenities (schools, hospitals, restaurants, parks, etc.)
- Water bodies (rivers, lakes, ponds)
- Boundaries (administrative)
- Public transport (bus routes, stops)
- POIs (Points of Interest)

**Download Methods:**

### 1. Geofabrik (India-wide):
- **URL:** https://download.geofabrik.de/asia/india.html
- **India-latest.osm.pbf:** 1.6 GB (updated daily)
- **Format:** .osm.pbf, .shp.zip, .gpkg.zip
- **Sub-regions:** Southern Zone includes Kerala
  - **Southern Zone:** https://download.geofabrik.de/asia/india/southern-zone.html
  - **Southern Zone .osm.pbf:** ~528 MB
  - **Southern Zone .gpkg.zip:** Available

### 2. Overpass API (City-specific queries):
- **URL:** https://overpass-api.de/api/interpreter
- Can query specific bounding boxes for each city

### 3. BBBike Extract Service:
- **URL:** https://extract.bbbike.org
- Create custom extracts for any city

**City Bounding Boxes (approximate):**
- **Thiruvananthapuram:** 8.4N - 8.6N, 76.8E - 77.0E
- **Kochi:** 9.8N - 10.1N, 76.2E - 76.4E
- **Kozhikode:** 11.1N - 11.3N, 75.7E - 75.9E

---

## 7. WIKIMEDIA COMMONS

**Categories with Georeferenced Photos:**

### Thiruvananthapuram:
- **Category:** https://commons.wikimedia.org/wiki/Category:Thiruvananthapuram
- **Files:** 255+ images
- **Subcategories:** Geography, Culture, Economy, Education, Structures, Nature, History, Transport
- **Coordinates:** Many images have GPS coordinates embedded
- **Wikidata:** Q167715

### Kochi:
- **Category:** https://commons.wikimedia.org/wiki/Category:Kochi,_Kerala
- **Files:** 78+ images (main category)
- **Subcategories:** 11 subcategories including Geography, Culture, Economy, Transport, Structures
- **Coordinates:** 9.97N, 76.28E
- **Wikidata:** Q1800

### Kozhikode:
- **Category:** https://commons.wikimedia.org/wiki/Category:Kozhikode
- **Files:** 46+ images (main category)
- **Subcategories:** 13 including Geography, Nature, History, Culture, Transport
- **Coordinates:** 11.25N, 75.78E
- **Wikidata:** Q28729

**Tools for Data Extraction:**
- **WikiShootMe:** https://wikishootme.toolforge.org
- **Locator Tool:** https://locator-tool.toolforge.org
- **KML Export:** https://kmlexport.toolforge.org
- **PetScan:** https://petscan.wmflabs.org

---

## 8. RESEARCH PAPERS & ACADEMIC SOURCES

**Key Research Papers Found (with URLs):**

### 1. Urban Sprawl in Thiruvananthapuram:
- **Title:** "Analyzing the urban sprawl-form and characteristics: a case study of Thiruvananthapuram, Kerala, India"
- **Authors:** BP Kumar, V Emayavaramban
- **Journal:** Journal of the Indian Society of Remote Sensing, 2023
- **PDF:** https://link.springer.com/article/10.1007/s12524-023-01781-2
- **Content:** GIS-based urban sprawl analysis with downloadable maps

### 2. GIS-based Land Suitability - Kochi:
- **Title:** "GIS based land suitability analysis for sustainable and resilient development in Vypin Island, Kochi, India"
- **Authors:** A Chandra, S Anilkumar
- **Year:** 2025
- **PDF:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5680942

### 3. Peri-Urban Development - Kozhikode:
- **Title:** "Geo-intelligence-based approach for sustainable development of peri-urban areas: A case study of Kozhikode City, Kerala (India)"
- **Authors:** VP Nishara, VS Krishnan, CM Firoz
- **Year:** 2021
- **PDF:** https://link.springer.com/chapter/10.1007/978-981-16-4768-0_3

### 4. Environmental Planning - Thiruvananthapuram:
- **Title:** "Environmental Planning Strategies for Resilient City: Case Study of Thiruvananthapuram, Kerala"
- **Authors:** A Sasi, A Raghava, J Sen
- **Year:** 2025
- **PDF:** https://link.springer.com/chapter/10.1007/978-981-97-8370-0_2

### 5. Coastal Vulnerability Analysis:
- **Title:** "An Integrated Coastal Vulnerability Analysis of Selected Coastal Areas of Kerala Using Bayesian Belief Network and GIS"
- **Authors:** G Gopinath, AL Achu, S Eldhose
- **Year:** 2026
- **Coverage:** Kozhikode, Ernakulam, Thiruvananthapuram districts

### 6. LULC Change - Kozhikode:
- **Title:** "Multi-temporal Dynamics of Land Use Land Cover Change and Urban Expansion in the Tropical Coastal District of Kozhikode"
- **Authors:** A Grover, A Vadakkuveettil
- **Year:** 2023
- **PDF:** https://link.springer.com/chapter/10.1007/978-3-031-21587-2_4

### 7. Urban Governance in Kerala:
- **Title:** "Ensuring sustainable urban governance: Insights from service delivery in Kerala"
- **Author:** V Vimal
- **Institution:** GIFT, Kerala
- **PDF:** https://www.gift.res.in/wp-content/uploads/2024/06/Ensuring-Sustainable-Urban-Governance-_Vimal-V.pdf

### 8. Metropolitan Development - Kozhikode:
- **Title:** "Smart Metropolitan Regional Development: Economic and Spatial Design Strategy for Kozhikode Metropolitan Region"
- **Authors:** TM Vinod Kumar, N Radhakrishnan, M Firoz
- **Year:** 2018
- **PDF:** https://link.springer.com/chapter/10.1007/978-981-10-8588-8_10

### 9. Urbanization Trends in Kerala:
- **Title:** "An Analysis of Trend and Spatial Pattern of Urbanization in Kerala with a Future Perspective"
- **Authors:** DV Surya, K Prakash, SR Jegankumar
- **Year:** 2024
- **PDF:** https://sciresol.s3.us-east-2.amazonaws.com/srs-j/bu_journals/GE/pdf/volume13/Issue-2/GE-2024-17.pdf

**Search Queries for More Papers:**
- Google Scholar: `https://scholar.google.com/scholar?q=GIS+Thiruvananthapuram+Kochi+Kozhikode+urban+planning`
- ResearchGate: Search for "Kerala urban planning GIS"
- Springer, Taylor & Francis, Elsevier: Search with city names + GIS/remote sensing

---

## 9. SOCIAL MEDIA SOURCES

**Instagram:**
- Geotags available for all 3 cities
- Search: `#Thiruvananthapuram`, `#Kochi`, `#Kozhikode`, `#Trivandrum`, `#Cochin`, `#Calicut`
- Location-based photo clusters
- Can scrape public data using APIs (with rate limits)

**YouTube:**
- Location-tagged videos available
- Search: City names + "drone", "aerial", "4K", "timelapse"
- Some channels: Kerala Tourism, Local news channels

**Flickr:**
- Many photos with EXIF GPS coordinates
- Search: Groups for Kerala photography

**Panoramio (archived):**
- Data migrated to Google Earth

**Important:** Social media scraping requires compliance with platform terms of service and data protection laws.

---

## 10. NEWS ARCHIVES

**The Hindu:**
- **URL:** https://www.thehindu.com
- Search: Kerala + city name + development projects
- Has archives dating back decades
- Topic: Urban development, infrastructure, planning

**Malayala Manorama:**
- **URL:** https://www.manoramaonline.com
- Major Malayalam newspaper
- Extensive coverage of local development
- English edition available

**Mathrubhumi:**
- **URL:** https://www.mathrubhumi.com
- Another major Malayalam daily
- Good for local project news

**The New Indian Express (Kerala):**
- Covers urban development, Smart City projects

**Kerala Government Press Release:**
- **URL:** https://www.prd.kerala.gov.in
- Official government announcements

**Important:** News archives may require subscription for full access. Many articles are behind paywalls.

---

## ADDITIONAL DATA SOURCES

### Census of India:
- **URL:** https://censusindia.gov.in (Transport error during research)
- **Data:** Population, housing, slum data, town directories
- **2011 Census:** Ward-level data for all 3 cities
- **2021 Census:** Currently being processed

### Data.gov.in (Open Government Data Platform):
- **URL:** https://data.gov.in
- **Kerala-specific datasets:** Search for Kerala state
- **Urban data:** Municipal corporation data, property tax, etc.
- **License:** Government Open Data License - India

### Kerala Institute of Local Administration (KILA):
- **URL:** https://www.kila.ac.in
- **Digital Repository:** http://dspace.kila.ac.in
- **Publications:** Local governance, urban planning studies
- **Training materials:** GIS, urban planning modules

### Kerala State Planning Board:
- **URL:** https://www.keralaplanningboard.org (Domain taken over - inaccessible)
- May have migrated to: https://spb.kerala.gov.in

### Survey of India:
- **Open Series Maps (OSM):** Available through Bhuvan
- **Topographic maps:** 1:50,000 scale
- **Can be purchased from:** SoI offices or through Bhuvan

### Copernicus/ESA (Europe):
- **Sentinel-2 data:** Free, 10m resolution
- **Sentinel-1 SAR data:** All-weather imaging
- **Access:** https://scihub.copernicus.eu
- **Coverage:** Complete coverage of Kerala, 5-day revisit

### USGS Earth Explorer:
- **Landsat data:** 1972-present, 30m resolution
- **ASTER GDEM:** 30m digital elevation model
- **URL:** https://earthexplorer.usgs.gov
- **Free registration required**

### NASA SRTM:
- **Digital Elevation Model:** 30m resolution
- **Coverage:** All of Kerala
- **Access:** Through Earth Explorer or Earth Engine

### Global Forest Watch:
- **Forest cover change data**
- **Powered by:** Google Earth Engine
- **URL:** https://www.globalforestwatch.org

### OpenAerialMap:
- **Drone imagery:** Some Kerala coverage
- **URL:** https://openaerialmap.org

### Humanitarian OpenStreetMap Team (HOT):
- **Kerala flood response:** 2018 floods mapped extensively
- **URL:** https://www.hotosm.org

### LandSAT Explorer:
- **Microsoft's tool:** https://landsatexplorer.earthengine.app
- **Easy visualization of Landsat data**

### Sentinel Hub:
- **Commercial but free tier available**
- **Sentinel data:** https://www.sentinel-hub.com

---

## SUMMARY OF DIRECT DOWNLOADS

### Immediate Access PDFs:
1. **Thiruvananthapuram Master Plan:** https://lsgd.kerala.gov.in/wp-content/uploads/2025/08/Thiruvananthapuram-City-Master-Plan.pdf
2. **Kochi Master Plan:** https://lsgd.kerala.gov.in/wp-content/uploads/2025/08/Kochi-City-Master-Plan.pdf
3. **Kozhikode Master Plan:** https://lsgd.kerala.gov.in/wp-content/uploads/2025/08/Kozhikode-Master-Plan.pdf
4. **Kerala Governance Report:** https://www.gift.res.in/wp-content/uploads/2024/06/Ensuring-Sustainable-Urban-Governance-_Vimal-V.pdf

### OpenStreetMap Data:
1. **India OSM:** https://download.geofabrik.de/asia/india-latest.osm.pbf
2. **Southern Zone:** https://download.geofabrik.de/asia/india/southern-zone-latest.osm.pbf

### Satellite Imagery:
1. **Google Earth Engine:** https://earthengine.google.com
2. **USGS Earth Explorer:** https://earthexplorer.usgs.gov
3. **Copernicus SciHub:** https://scihub.copernicus.eu

### Research Papers:
1. **Thiruvananthapuram Sprawl:** https://link.springer.com/article/10.1007/s12524-023-01781-2
2. **Kochi Land Suitability:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5680942
3. **Kozhikode Peri-Urban:** https://link.springer.com/chapter/10.1007/978-981-16-4768-0_3

### Wikimedia Commons:
1. **Thiruvananthapuram:** https://commons.wikimedia.org/wiki/Category:Thiruvananthapuram
2. **Kochi:** https://commons.wikimedia.org/wiki/Category:Kochi,_Kerala
3. **Kozhikode:** https://commons.wikimedia.org/wiki/Category:Kozhikode

---

## DATA QUALITY NOTES

**Strengths:**
- Master plans are official, recent, and comprehensive
- OpenStreetMap has good community coverage
- Satellite imagery is abundant and freely available
- Research papers provide academic analysis

**Gaps:**
- KSDI portal was inaccessible - may require government access or is under maintenance
- Bhuvan Kerala requires specific plugins/registration
- Smart City documents may require RTI or direct city corporation contact
- Real-time cadastral data is not publicly available online
- Street View coverage is limited compared to Western cities
- Some news archives require paid subscriptions

**Recommendations:**
1. Download master plans immediately (PDFs are confirmed working)
2. Use Google Earth Engine for historical satellite analysis
3. Extract OSM data via Geofabrik for current land use/buildings
4. Contact Kerala Town Planning Department for cadastral data
5. Use Google Scholar to access full-text of research papers
6. For social media, use official APIs with proper authentication

---

*Report compiled on: 11 June 2026*
*Note: Some government portals may have intermittent access. PDF links were verified during research.*
