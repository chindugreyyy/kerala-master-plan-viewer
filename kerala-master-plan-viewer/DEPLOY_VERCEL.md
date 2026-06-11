# Deploy to Vercel with Custom Domain (maps.keralafirst.co.in)

## 🎯 Overview

You want to deploy the Kerala Master Plan Viewer to **Vercel** and make it accessible at:
```
https://maps.keralafirst.co.in
```

This is actually the **best** deployment strategy. Here's why:

| Feature | GitHub Pages | Vercel |
|---------|-------------|--------|
| HTTPS | ✅ Yes | ✅ Yes (Auto) |
| Custom Domain | ✅ Yes | ✅ Yes (Easier) |
| CDN | ❌ Basic | ✅ Global Edge Network |
| Speed | Good | ⚡ Faster (Global) |
| SSL | Manual | ✅ Auto-renew |
| Analytics | ❌ | ✅ Built-in |
| Preview URLs | ❌ | ✅ Per commit |
| Serverless | ❌ | ✅ Functions ready |

---

## 🚀 Step 1: Create Vercel Account

### Option A: Sign Up with GitHub (Recommended)
1. Go to **[vercel.com](https://vercel.com)**
2. Click **"Sign Up"**
3. Select **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account
   - Choose **"All repositories"** or **"Only select repositories"**
   - If select: Choose `Chindugrey/keralafirst-cities`

### Option B: Email Sign Up
1. Go to **[vercel.com](https://vercel.com)**
2. Click **"Sign Up"**
3. Enter your email
4. Verify email
5. Connect GitHub later in settings

---

## 🚀 Step 2: Import Your GitHub Repo

1. After signing in, click **"Add New Project"** on the dashboard
2. You'll see your GitHub repos listed
3. Find and select **`keralafirst-cities`**
4. Click **"Import"**

### Configure Project Settings:

**Project Name:** `kerala-master-plan` (or whatever you prefer)

**Framework Preset:** `Other` (or `Create React App` if that appears)

**Root Directory:** `./` (leave as default)

**Build Command:** Leave empty (it's static HTML)

**Output Directory:** Leave empty (or set to `.`)

**Install Command:** `npm install` (or leave empty)

5. Click **"Deploy"**

⏱️ **Wait 1-2 minutes** for deployment...

✅ **Success!** You'll see a URL like:
```
https://kerala-master-plan.vercel.app
```

**Click the URL to verify it works!**

---

## 🚀 Step 3: Add Custom Domain (maps.keralafirst.co.in)

### 3.1 Go to Project Settings
1. In your Vercel project, click **"Settings"** tab
2. Click **"Domains"** in the left sidebar
3. Click **"Add Domain"**

### 3.2 Enter Your Domain
```
maps.keralafirst.co.in
```

### 3.3 Vercel Will Show You DNS Records

Vercel will display something like this:

**For Subdomain (maps.keralafirst.co.in):**
```
Type: CNAME
Name: maps
Value: cname.vercel-dns.com
```

**Or if you want to use A Record (for root domain):**
```
Type: A
Name: @
Value: 76.76.21.21
```

**Keep this page open** — you'll need these values for Step 4.

---

## 🚀 Step 4: Update DNS in Your Domain Registrar

You need to add a DNS record wherever you manage `keralafirst.co.in`.

### Common Places:

| Where You Bought Domain | Where to Manage DNS |
|-------------------------|---------------------|
| GoDaddy | GoDaddy DNS Management |
| Namecheap | Namecheap Advanced DNS |
| Google Domains | Google Domains DNS |
| Cloudflare | Cloudflare DNS |
| Hostinger | Hostinger DNS |
| cPanel (shared hosting) | cPanel → Zone Editor |

### What to Add (CNAME Record):

```
Type: CNAME
Name: maps
Value: cname.vercel-dns.com
TTL: 3600 (or Auto)
```

### Example for cPanel:
1. Log in to your hosting account
2. Go to **cPanel**
3. Find **"Zone Editor"** or **"DNS Zone Editor"**
4. Select domain: `keralafirst.co.in`
5. Click **"Add Record"**
6. Type: **CNAME**
7. Name: **maps**
8. Value: **cname.vercel-dns.com**
9. TTL: **3600**
10. Click **"Add Record"**

### Example for Cloudflare:
1. Log in to Cloudflare
2. Select `keralafirst.co.in`
3. Go to **DNS** tab
4. Click **"Add Record"**
5. Type: **CNAME**
6. Name: **maps**
7. Target: **cname.vercel-dns.com**
8. TTL: **Auto**
9. Proxy status: **DNS only** (gray cloud, NOT orange!)
10. Click **"Save"**

### Example for GoDaddy:
1. Log in to GoDaddy
2. Go to **My Products** → **DNS**
3. Find **"Manage"** next to `keralafirst.co.in`
4. Scroll to **"Records"**
5. Click **"Add"**
6. Type: **CNAME**
7. Name: **maps**
8. Value: **cname.vercel-dns.com**
9. TTL: **1 Hour**
10. Click **"Save"**

---

## 🚀 Step 5: Verify Domain in Vercel

1. Go back to the Vercel tab where you added the domain
2. Click **"Verify"** or **"Refresh"**
3. Vercel will check if the DNS record is correct

### Possible Statuses:

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ **Valid** | Domain is connected! | You're done! |
| ⏳ **Pending** | DNS propagating | Wait 5-30 minutes |
| ❌ **Invalid** | DNS record wrong | Double-check Step 4 |

### If it says "Invalid":
1. Double-check the CNAME value (must be `cname.vercel-dns.com`)
2. Make sure there's no typo in the Name field (`maps`)
3. Wait 10 minutes and click "Verify" again
4. DNS propagation takes time (up to 48 hours, usually 5-30 minutes)

---

## 🚀 Step 6: Enable HTTPS (SSL)

**Vercel automatically provides SSL** for custom domains!

1. In Vercel → Settings → Domains
2. Find `maps.keralafirst.co.in`
3. Click **"Enable HTTPS"** (if not auto-enabled)
4. Vercel will generate a **free SSL certificate** via Let's Encrypt
5. Wait 2-3 minutes

✅ **Your site is now live at:**
```
https://maps.keralafirst.co.in
```

---

## 🚀 Step 7: Test Everything

### Test URLs:
1. **Main Viewer:** `https://maps.keralafirst.co.in`
2. **Admin Dashboard:** `https://maps.keralafirst.co.in/admin`
3. **Cities JSON:** `https://maps.keralafirst.co.in/cities.json`

### What to Verify:
- ✅ Page loads without errors
- ✅ Map shows Kerala
- ✅ City selector works
- ✅ Proxy layer loads (select a city, wait 5-10 seconds)
- ✅ Legend appears
- ✅ Data source badge shows "Current Land Use (Proxy)"
- ✅ Admin dashboard loads
- ✅ HTTPS is active (lock icon in browser)

---

## 🚀 Step 8: Configure GitHub Auto-Deploy (Optional)

**Vercel already auto-deploys** when you push to GitHub!

### Every Time You Push to `main`:
1. Vercel detects the push
2. Builds the project
3. Deploys to `maps.keralafirst.co.in`
4. You get a **Preview URL** for the commit

### To Check:
1. In Vercel project → **"Deployments"** tab
2. You'll see every commit listed
3. Click any commit to see its preview URL

---

## 🚀 Step 9: Set Up Environment Variables (Optional)

If you add a backend later (Supabase, etc.):

1. Vercel → Settings → **Environment Variables**
2. Add:
   - `SUPABASE_URL` = your Supabase URL
   - `SUPABASE_ANON_KEY` = your anon key
3. Click **"Save"**

---

## 🚀 Step 10: Add Analytics (Optional)

1. Vercel → **Analytics** tab
2. Click **"Enable"**
3. See real-time visitors, page views, performance

---

## 🔧 Troubleshooting

### Problem: "Domain not found" or "DNS not resolving"

**Solution:**
1. Check DNS record in your registrar (Step 4)
2. Use `dig` or `nslookup` to verify:
   ```bash
   dig maps.keralafirst.co.in CNAME
   ```
   Should show: `cname.vercel-dns.com`
3. Wait longer (DNS can take 24-48 hours)
4. Try clearing DNS cache:
   ```bash
   # macOS
   sudo dscacheutil -flushcache
   
   # Windows
   ipconfig /flushdns
   ```

### Problem: "SSL certificate not valid"

**Solution:**
1. In Vercel → Settings → Domains
2. Find `maps.keralafirst.co.in`
3. Click **"Remove"** then **"Add"** again
4. Wait 5 minutes

### Problem: "404 when visiting /admin"

**Solution:**
1. Check `vercel.json` routes
2. Make sure `admin.html` is in the repo
3. Redeploy:
   ```bash
   git commit --allow-empty -m "Trigger redeploy"
   git push origin main
   ```

### Problem: "Proxy layer not loading"

**Solution:**
1. Open browser console (F12)
2. Check for CORS errors or network failures
3. Overpass API might be rate-limited
4. Wait 30 seconds and try again

### Problem: "Changes not showing after git push"

**Solution:**
1. Vercel deployments take 30-60 seconds
2. Check Vercel dashboard → Deployments
3. If stuck, click **"Redeploy"** on the latest commit

---

## 📝 Quick Reference: Files You Need

```
vercel.json          ✅  (Already in repo)
package.json         ✅  (Already in repo)
CNAME                ✅  (Already in repo)
index.html           ✅  (Already in repo)
main.js              ✅  (Already in repo)
style.css            ✅  (Already in repo)
proxy-layer.js       ✅  (Already in repo)
admin.html           ✅  (Already in repo)
cities.json          ✅  (Already in repo)
```

---

## 🎯 What You Need to Do (Summary)

| Step | Action | Time |
|------|--------|------|
| 1 | Sign up at [vercel.com](https://vercel.com) with GitHub | 2 min |
| 2 | Import `keralafirst-cities` repo | 2 min |
| 3 | Add domain `maps.keralafirst.co.in` in Vercel | 2 min |
| 4 | Add CNAME DNS record in your registrar | 3 min |
| 5 | Wait for DNS propagation | 5-30 min |
| 6 | Verify domain in Vercel | 1 min |
| 7 | Test `https://maps.keralafirst.co.in` | 2 min |

**Total time: 15-45 minutes**

---

## 🎉 After Deployment

Your viewer will be live at:
```
https://maps.keralafirst.co.in
```

And you can update it by simply:
```bash
git add .
git commit -m "Update cities"
git push origin main
```

**Vercel will auto-deploy every push!**

---

## 💡 Next: Add a Backend

Once deployed, you can add:
- **Supabase** for comments (free tier)
- **Vercel Serverless Functions** for form submissions
- **Vercel Analytics** for visitor tracking

All included in the free plan.

---

**Questions?** Check [Vercel Docs](https://vercel.com/docs) or [Vercel Discord](https://vercel.com/discord)

**Ready to deploy?** Start with Step 1: [vercel.com](https://vercel.com)
