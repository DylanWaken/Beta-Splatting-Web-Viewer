# Quick Start Guide - GitHub Pages Deployment

Get your Beta Splatting Web Viewer live in 5 minutes!

## Prerequisites
- GitHub account
- Git installed
- This repository on your computer

## Deploy in 3 Steps

### Step 1: Push to GitHub (if not done already)

```bash
# Navigate to your project
cd Beta-Splatting-Web-Viewer

# Add all files
git add .

# Commit
git commit -m "Ready for GitHub Pages"

# Push to GitHub
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repo: `github.com/DylanWaken/Beta-Splatting-Web-Viewer`
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Source", select: **GitHub Actions**
5. Done!

### Step 3: Wait & Visit

1. Go to **Actions** tab
2. Watch deployment (1-2 minutes)
3. Visit: `https://DylanWaken.github.io/Beta-Splatting-Web-Viewer/`

## That's It!

Your 3D viewer is now live on the internet!

---

## Test Locally First (Optional)

Before deploying, test on your computer:

```bash
# Start server
python -m http.server 8080

# Visit in browser
http://localhost:8080
```

Press Ctrl+C to stop the server.

---

## Customize

### Change the Default Model

Edit `index.html`, line 38:
```javascript
let path = 'web/assets/bs/point_cloud.ply';  // ← Change this
```

### Add Your Own PLY File

1. Put your `.ply` file in `web/assets/bs/`
2. Update the path in `index.html`
3. Push changes:
```bash
git add .
git commit -m "Add new model"
git push origin main
```

GitHub will automatically redeploy!

---

## Share Your Viewer

Your live URL:
```
https://DylanWaken.github.io/Beta-Splatting-Web-Viewer/
```

Share on:
- Twitter/X
- LinkedIn  
- Portfolio
- Research papers
- Presentations

---

## Troubleshooting

### Site not loading?
- Wait 5 minutes after first deployment
- Clear browser cache (Ctrl+Shift+R)
- Check Actions tab for errors

### Model not showing?
- Verify file path in `index.html`
- Check browser console (F12) for errors
- Ensure PLY file is in `web/assets/bs/`

### Need more help?
- See `DEPLOYMENT.md` for detailed guide
- Check `DEPLOYMENT_CHECKLIST.md`
- Review `README.md`

---

## Next Steps

- [ ] Test your deployed site
- [ ] Add your own models
- [ ] Customize camera settings
- [ ] Share with colleagues
- [ ] Star the repo

---

## Learn More

- **Full Deployment Guide**: `DEPLOYMENT.md`
- **Complete README**: `README.md`
- **Migration Details**: `MIGRATION_SUMMARY.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`

---

**Made with love using Three.js and GitHub Pages**

Happy viewing!

