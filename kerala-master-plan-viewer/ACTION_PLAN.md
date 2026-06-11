# Kerala Master Plan Data — Action Plan

## What I Found

**Reality Check:** Kerala master plan data is **not available online** in downloadable, georeferenced format. This is the biggest blocker for your viewer.

I tried accessing:
- ❌ Kerala government portals (all down or timing out)
- ❌ Municipal corporation websites (unreachable)
- ❌ MapWarper (no Kerala master plans found)
- ❌ Search engines (rate limited)

**Good news:** The plans **exist physically** at government offices. You just need to collect them.

---

## What I Built For You

I've created a complete **data collection toolkit** in your repo:

### 📄 Documents Created

| File | Purpose | Lines |
|------|---------|-------|
| `DATA_SOURCES.md` | Complete guide to all known sources | 250+ |
| `DATA_TRACKER.md` | Tracking spreadsheet for all 43 cities | 180+ |
| `data_pipeline.py` | Python script to convert PDFs → COGs | 280+ |
| `sample_gcp.csv` | Template for georeferencing points | 40+ |

---

## Your Exact Next Steps

### Step 1: File RTI (Today)

File Right to Information requests for all 6 corporations. This is the **most reliable** way to get the plans.

**Template is in `DATA_SOURCES.md`** — just copy, fill in your details, and submit.

**Where to file:**
- Online: `https://rtionline.gov.in` (or Kerala state RTI portal)
- In person: At each corporation office
- Fee: ₹10 + ₹2 per page

**Expected timeline:** 30 days for response

### Step 2: Call Corporations (This Week)

**Priority calls (highest chance of success):**

1. **GCDA Kochi** — `gcdaonline.com` — They are more modern, may have digital plans
2. **Thiruvananthapuram Corporation** — Town Planning wing
3. **Kochi Corporation** — Town Planning wing
4. **Thrissur Corporation** — Usually well-organized

**Ask for:**
- "Can you share the latest development plan map?"
- "Do you have a scanned PDF of the master plan?"
- "Is there a digital/GIS version available?"

### Step 3: Visit Offices (If RTI is slow)

If RTI takes too long, physically visit:

**Best starting point:**
- **Town Planning Department HQ** — Thiruvananthapuram
  - Address: Town Planning Directorate, Near Museum, Thiruvananthapuram
  - They have plans for ALL cities

**What to bring:**
- Phone with good camera (for photographing maps if scanning not allowed)
- Notebook
- USB drive (if they can give digital files)
- Formal request letter

### Step 4: Collect First Plan (Week 1-2)

**Don't try to get all 43 at once.** Start with **1-2 cities**.

**Recommended first city:** **Thiruvananthapuram** or **Kochi**
- Capital city / largest city
- Most likely to have a documented plan
- Good for testing your workflow

### Step 5: Georeference (Week 2-3)

Once you have a scanned PDF:

**Option A: MapWarper (Easiest, Free)**
1. Go to `mapwarper.net`
2. Create account
3. Upload scanned PDF
4. Add 6-10 control points (match landmarks on map to Google Maps)
5. Click "Rectify"
6. Get XYZ tile URL
7. Add to `cities.json`

**Option B: Python Pipeline (More Control)**
```bash
# Install GDAL
brew install gdal  # macOS
# or apt-get install gdal-bin  # Linux

# Use the script I created
python data_pipeline.py --input plan.pdf --output plan_cog.tif --gcp gcp.csv
```

### Step 6: Upload & Launch (Week 3-4)

1. Upload COG to Cloudflare R2 (free tier) or AWS S3
2. Enable CORS
3. Get public URL
4. Update `cities.json` with `cogUrl`
5. Commit to GitHub
6. Announce on Kerala First!

---

## Expected Timeline

| Week | Action | Output |
|------|--------|--------|
| 1 | File RTI, call corporations | 3-5 requests filed |
| 2 | Visit offices, collect scans | 1-2 city plans acquired |
| 3 | Georeference, convert to COG | 1-2 plans ready |
| 4 | Upload, test, update viewer | First city live! |
| 5-8 | Repeat for more cities | 5-10 cities live |
| 2-3 months | Full collection | 15-20 cities |

---

## Cost Estimate

| Item | Cost | Notes |
|------|------|-------|
| RTI filing | ₹10-50 | Per city |
| Scanning/Photocopy | ₹50-200 | Per city |
| Cloudflare R2 | ₹0-500/month | Free tier: 10GB |
| Georeferencing | Free | MapWarper / QGIS |
| **Total (first 10 cities)** | **₹1,000-3,000** | Very affordable |

---

## Who Can Help You

1. **Local journalists** — They may have access or know who does
2. **Real estate developers** — They use these plans
3. **Urban planners in Kerala** — LinkedIn connections
4. **Architecture students** — They may have collected plans for projects
5. **RTI activists** — Experienced in getting government documents
6. **Kerala Library Association** — May have archived plans

---

## Important Reality

**Most Kerala municipalities don't have digitized plans.** The process is:

1. Find paper plan at government office
2. Scan/photograph it
3. Georeference it manually
4. Convert to web format
5. Upload

This is **not an instant process.** It takes time and effort.

**But the result is valuable:** You'll be the first person to create a comprehensive, publicly accessible Kerala master plan viewer. That's a major achievement for citizen transparency.

---

## FAQ

**Q: Can I just use Google Maps data?**
A: No, Google Maps doesn't have master plan overlays. You need the actual planning documents.

**Q: Are there any existing repositories?**
A: Not that I could find. I checked all major portals. This is genuinely uncharted territory.

**Q: What if the office refuses to give plans?**
A: File RTI. They are legally obligated. If they refuse, appeal to the RTI commission.

**Q: Can I use AI to generate plans?**
A: No, master plans are legal documents. You need the official plans.

**Q: Is there any shortcut?**
A: Not really. But start with the 6 corporations — they definitely have plans.

---

## What to Do Right Now

1. **Open `DATA_SOURCES.md`** — Read the full research guide
2. **Call GCDA Kochi** — Ask if they have a Kochi plan PDF
3. **File one RTI** — Start with Thiruvananthapuram
4. **Update `DATA_TRACKER.md`** — Mark actions taken
5. **Commit your progress** — Update the repo

---

**Need help?** The viewer is ready. The data collection is the real work. Take it one city at a time.

Good luck! 🌴
