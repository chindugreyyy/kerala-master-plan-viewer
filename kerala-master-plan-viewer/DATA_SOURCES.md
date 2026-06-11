# Kerala Master Plan Data Sources — Research Guide

**Last Updated:** 2026-06-11
**Status:** Active research in progress

---

## Summary

Kerala master plan data is **not readily available online** in georeferenced format. Most plans exist as:
- Physical documents at Town Planning offices
- Scanned PDFs on government websites (often not georeferenced)
- Internal CAD files at municipal corporations

This guide documents all known sources and strategies to acquire them.

---

## 🔴 Why Kerala Plans Are Hard to Find

1. **No centralized GIS portal** — Unlike some states (Karnataka, Maharashtra), Kerala doesn't have a comprehensive online GIS repository for all city plans
2. **Government websites unreliable** — Many portals are offline or poorly maintained
3. **Plans are not digitized** — Most town plans are still paper-based
4. **No open data initiative** — Kerala has limited open geospatial data

---

## 🟢 Known Data Sources (Verified & Likely)

### 1. Kerala State Town Planning Department
**Primary authority for all Kerala development plans**

- **Website:** `https://tsp.kerala.gov.in` (often offline)
- **Contact:** Town Planning Department, Government of Kerala
  - Address: Town Planning Directorate, Thiruvananthapuram
  - Phone: +91-471-2323015 (verify current)
- **What they have:** Master plans for all 6 corporations and many municipalities
- **How to access:** 
  - Visit office in person
  - File RTI application
  - Request scanned copies

### 2. Individual Municipal Corporations

Each corporation maintains their own development plan:

| Corporation | Website | Contact | Likely Has Plan? |
|-------------|---------|---------|------------------|
| **Thiruvananthapuram** | `corporationoftrivandrum.org` | Corporation Office, Palayam | ✅ Yes |
| **Kochi** | `kochicorporation.gov.in` | Ernakulam, near Town Hall | ✅ Yes |
| **Kozhikode** | `kozhikodecorporation.in` | Near Beach | ✅ Yes |
| **Kollam** | `kollamcorporation.gov.in` | Near KSRTC | ✅ Yes |
| **Thrissur** | `thrissurcorporation.org` | Near Swaraj Round | ✅ Yes |
| **Kannur** | `kannurcorporation.gov.in` | Near Fort Road | ✅ Yes |

**Strategy:** Visit each corporation's Town Planning Department office. Request:
- Development Plan (DP) maps
- Land use maps
- Road network plans
- Zoning plans

### 3. Kerala Town & Country Planning Department (KTCP)
- **District offices:** Each district has a KTCP office
- **What they have:** District plans, town plans for municipalities
- **Access:** Physical visit + RTI

### 4. Kerala State Spatial Data Infrastructure (KSDI)
- **Portal:** GIS portal for Kerala (URL varies, often under ksdikerala.org)
- **What they might have:** Some base layers, but rarely master plans
- **Status:** Limited availability

### 5. Bhuvan Kerala (ISRO)
- **Portal:** `bhuvan.nrsc.gov.in` → Kerala section
- **What they have:** Satellite imagery, some base maps
- **Not useful for:** Master plan overlays (don't have planning data)

### 6. GCDA (Greater Cochin Development Authority)
- **Area:** Kochi region
- **What they have:** Kochi regional plan
- **Contact:** `gcdaonline.com` or visit office
- **Status:** May have some digitized plans

### 7. KITCO
- **Kerala Industrial & Technical Consultancy Organisation**
- **What they have:** Some planning documents for various projects
- **Contact:** `kitco.in`
- **Status:** May help with sourcing plans

---

## 🟡 Potential Sources (Need Verification)

### 8. Academic Institutions
- **NIT Calicut** — Urban planning department may have research data
- **IIT Palakkad** — May have geospatial projects
- **CUSAT** — Center for Science in Society
- **MG University** — Geography department

**Strategy:** Contact professors in urban planning/geography departments

### 9. Research Papers
Search for:
- "Kerala urban planning" on ResearchGate, Google Scholar
- "Kochi development plan" academic papers
- "Kerala master plan GIS" research

**Note:** Researchers may have digitized data but not published it as downloadable maps

### 10. GIS Companies in Kerala
- **Companies like:** InfoPark companies, GIS consultancies in Kochi
- **Strategy:** They may have georeferenced data for projects

### 11. OpenStreetMap Community
- **Kerala OSM community** may have traced some land use data
- **Not master plans** but could be useful for comparison

---

## 🔵 Strategy to Acquire Data

### Phase 1: Quick Wins (1-2 weeks)
1. **Call/Email all 6 corporations** — Ask if they have PDFs of development plans
2. **File RTI** — Request development plans for all 43 cities
3. **Check Google** — Search for "{city name} master plan PDF site:gov.in"
4. **Check MapWarper** — Search for any Kerala plans already uploaded

### Phase 2: Physical Collection (2-4 weeks)
1. **Visit Thiruvananthapuram** — Town Planning Directorate HQ
2. **Visit district offices** — Collect plans for nearby towns
3. **Scan documents** — Use high-resolution scanner (300+ DPI)
4. **Photograph** — If scanning not allowed, use camera

### Phase 3: Georeferencing (4-8 weeks)
1. **MapWarper** — Upload scanned PDFs, georeference
2. **QGIS** — More precise georeferencing
3. **Convert to COG** — Using GDAL
4. **Upload to cloud** — R2 or S3
5. **Update viewer** — Add URLs to cities.json

---

## 🟠 RTI Template

**To:** Public Information Officer, Town Planning Department, Kerala

**Subject:** Request for development plan/master plan documents

**Request:**
I am seeking copies of the approved development plans/master plans for the following cities/towns in Kerala:
1. Thiruvananthapuram
2. Kochi
3. Kozhikode
4. Kollam
5. Thrissur
6. Kannur
7. Alappuzha
8. Palakkad
9. Malappuram
10. Kottayam
11. Pathanamthitta
12. Idukki
13. Wayanad
14. Kasaragod
15. [Add other towns]

Please provide:
- Latest approved development plan maps
- Land use classification maps
- Road network plans
- Zoning plans

Format: Scanned PDF copies or digital files if available

**Fee:** Include Rs. 10 application fee + Rs. 2 per page copying fee

---

## 📊 Data Collection Tracker

| City/Town | Status | Source | Contact | Notes |
|-------------|--------|--------|---------|-------|
| Thiruvananthapuram | 🔴 Not sourced | Trivandrum Corp | Pending | |
| Kochi | 🔴 Not sourced | Kochi Corp / GCDA | Pending | |
| Kozhikode | 🔴 Not sourced | Kozhikode Corp | Pending | |
| Kollam | 🔴 Not sourced | Kollam Corp | Pending | |
| Thrissur | 🔴 Not sourced | Thrissur Corp | Pending | |
| Kannur | 🔴 Not sourced | Kannur Corp | Pending | |
| Alappuzha | 🔴 Not sourced | Municipality | Pending | |
| Palakkad | 🔴 Not sourced | Municipality | Pending | |
| Malappuram | 🔴 Not sourced | Municipality | Pending | |
| Kottayam | 🔴 Not sourced | Municipality | Pending | |
| Pathanamthitta | 🔴 Not sourced | Municipality | Pending | |
| Idukki | 🔴 Not sourced | Municipality | Pending | |
| Wayanad | 🔴 Not sourced | Municipality | Pending | |
| Kasaragod | 🔴 Not sourced | Municipality | Pending | |
| Ponnani | 🔴 Not sourced | Municipality | Pending | |
| [Others] | 🔴 Not sourced | [Pending] | Pending | |

---

## 🛠️ Tools for Data Collection

### Visiting Offices
- **High-res camera** (20MP+) for photographing maps
- **Portable scanner** (if allowed)
- **GPS device** for recording map corner coordinates
- **Notebook** for documenting sources

### Once You Have PDFs
- **MapWarper** (free, web-based) for quick georeferencing
- **QGIS** (free, desktop) for precise georeferencing
- **GDAL** (command line) for COG conversion
- **Cloudflare R2** or **AWS S3** for hosting

---

## 💡 Pro Tips

1. **Start with one city** — Don't try to collect all at once. Begin with Thiruvananthapuram or Kochi
2. **Network with planners** — Connect with Kerala urban planners on LinkedIn
3. **Attend workshops** — Town Planning Department sometimes holds public meetings
4. **Check newspapers** — Plans are published in gazettes for public comment
5. **Ask academics** — PhD students may have digitized data
6. **Consider crowdsourcing** — If you have scanned plans, volunteers can help georeference
7. **Use KLA connection** — Kerala Library Association may have archived plans

---

## 📞 Priority Contacts

### Must-Call (High Probability of Success)
1. **Town Planning Department HQ** — Thiruvananthapuram
2. **GCDA** — Kochi (they're more modern)
3. **Thiruvananthapuram Corporation** — Town Planning wing
4. **Kochi Corporation** — Town Planning wing

### Secondary
5. **Kannur Corporation** — Often well-organized
6. **Thrissur Corporation** — Active planning
7. **Kozhikode Corporation** — Progressive municipality

---

## 🌐 Useful URLs

- Kerala Govt Portal: `https://www.kerala.gov.in` (verify working)
- Town Planning: `https://tsp.kerala.gov.in` (verify working)
- KSDI: `https://ksdi.kerala.gov.in` (verify working)
- KITCO: `https://www.kitco.in`
- GCDA: `https://gcdaonline.com`
- Bhuvan: `https://bhuvan.nrsc.gov.in`

---

## 🎯 Recommended First Steps

1. **Today:** Call GCDA Kochi — ask if they have digitized Kochi plans
2. **This week:** File RTI for all 6 corporation plans
3. **Next week:** Visit Thiruvananthapuram Town Planning office
4. **Month 1:** Collect and scan plans for 3-5 major cities
5. **Month 2:** Georeference and upload first batch

---

## ⚠️ Legal Note

Development plans are **public documents** under the Right to Information Act. Citizens have the right to access them. However, some municipalities may resist sharing. Be polite but persistent. Mention that the plan is already a public document published for public comment.

---

**Next:** Once you have scanned plans, see `DATA_GUIDE.md` for georeferencing instructions.
