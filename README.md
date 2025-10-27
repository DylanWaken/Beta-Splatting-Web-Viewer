# beta-splatting-webviewer

A DBS (Dynamic Beta Splatting) web viewer built with Three.js. Now deployable as a static site on GitHub Pages!

![webview](/assets/webview.png)

## 🚀 Live Demo

Visit the live demo: `https://YOUR_USERNAME.github.io/Beta-Splatting-Web-Viewer/`

## 📦 Quick Start (Local Development)

No server needed! Just open the files locally:

### Option 1: Using Python's built-in server
```bash
python -m http.server 8080
```
Then navigate to `http://localhost:8080`

### Option 2: Using Node.js http-server
```bash
npx http-server -p 8080
```

### Option 3: Using VS Code Live Server
Install the "Live Server" extension and click "Go Live" at the bottom right.

### Option 4: Direct file access (may have CORS issues)
Simply open `index.html` in your browser (some features may not work due to CORS restrictions).

## 🌐 Deploy to GitHub Pages

### Method 1: GitHub Actions (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for GitHub Pages deployment"
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Source", select **GitHub Actions**

3. **Deploy using the workflow:**
   The included `.github/workflows/deploy.yml` will automatically deploy your site on every push to main.

### Method 2: Manual Deployment

1. **Enable GitHub Pages:**
   - Go to your repository settings
   - Navigate to **Pages**
   - Under "Source", select **main branch** and **/ (root)** folder
   - Click Save

2. **Your site will be live at:**
   `https://YOUR_USERNAME.github.io/REPOSITORY_NAME/`

### Method 3: Deploy to gh-pages branch

```bash
# Install gh-pages if you haven't
npm install -g gh-pages

# Deploy
gh-pages -d . -b gh-pages
```

Then set GitHub Pages to use the `gh-pages` branch in repository settings.

## 📁 Project Structure

```
Beta-Splatting-Web-Viewer/
├── index.html              # Main entry point (GitHub Pages serves this)
├── web/                    # Frontend web viewer
│   ├── betaindex.html      # Original Beta Splatting viewer
│   ├── betaviewSB.js       # Beta Splatting viewer module (442KB)
│   ├── three.module.js     # Three.js library
│   └── assets/             # PLY files and assets
│       ├── bs/             # Beta Splatting files
│       │   ├── point_cloud.ply
│       │   └── RA_DBS_point_cloud.ply
│       └── gs/             # Gaussian Splatting files
│           └── lego.ply
├── flaskhost/              # Legacy Flask backend (not needed for GitHub Pages)
├── .nojekyll               # Tells GitHub Pages not to process files with Jekyll
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions deployment workflow
└── README.md               # This file
```

## 🎮 How to Use

### Adding Your Own PLY Files

1. **For Beta Splatting (DBS) files:**
   - Place your PLY file in `web/assets/bs/`
   - Update the path in `index.html`:
     ```javascript
     let path = 'web/assets/bs/your_file.ply';
     ```

2. **For standard Gaussian Splatting files:**
   - Place your PLY file in `web/assets/gs/`
   - Update the path accordingly

### Camera Settings

Modify camera parameters in `index.html`:

```javascript
const viewer = new BetaView.Viewer({
    'cameraUp': [0, 0, 1],              // Camera up vector
    'initialCameraPosition': [0, 1, 0], // Starting position
    'initialCameraLookAt': [1, 0, 0],   // Look at point
});
```

### Controls

- **Left Mouse Button:** Rotate camera
- **Right Mouse Button:** Pan camera
- **Mouse Wheel:** Zoom in/out
- **Touch Gestures:** Supported on mobile devices

## 🔧 Customization

### Change the Default Model

Edit `index.html` and modify the path:

```javascript
let path = 'web/assets/bs/point_cloud.ply';  // Change this line
```

### Add Multiple Models

You can extend the viewer to support multiple models with a dropdown or buttons. Example:

```javascript
const models = {
  'model1': 'web/assets/bs/point_cloud.ply',
  'model2': 'web/assets/bs/RA_DBS_point_cloud.ply'
};

// Add UI controls to switch between models
```

## 🐛 Troubleshooting

### PLY file not loading
- Verify the file path in the HTML file matches your PLY location
- Check browser console (F12) for error messages
- Ensure the PLY file is in the correct format
- Make sure you're running through a web server (not file://)

### Performance issues
- Try reducing the size of the PLY file
- Use the streaming view option: `'streamView': true`
- Close other browser tabs consuming resources
- Enable hardware acceleration in browser settings

### Browser compatibility
- Use the latest version of Chrome, Firefox, Edge, or Safari
- Enable WebGL in your browser settings
- Check if hardware acceleration is enabled

### GitHub Pages specific issues

**Site not updating:**
- Clear your browser cache
- Wait a few minutes for GitHub to rebuild
- Check the Actions tab for build errors

**404 errors on assets:**
- Verify file paths are relative (no leading `/`)
- Check file names are case-sensitive
- Ensure `.nojekyll` file exists in root

**CORS issues:**
- Should not occur on GitHub Pages (same origin)
- If testing locally, use a local server (not file://)

## 🏗️ Development

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Beta-Splatting-Web-Viewer.git
   cd Beta-Splatting-Web-Viewer
   ```

2. **Start a local server:**
   ```bash
   python -m http.server 8080
   ```

3. **Open in browser:**
   Navigate to `http://localhost:8080`

### Testing Before Deployment

Always test locally before pushing to GitHub:

```bash
# Start local server
python -m http.server 8080

# Test in browser at http://localhost:8080
# Check browser console for errors
# Verify all models load correctly
```

## 📝 Migration Notes

This project has been refactored from a Flask-based backend to a pure static site for GitHub Pages deployment:

- ✅ **Removed:** Flask backend dependencies
- ✅ **Simplified:** Direct static file serving
- ✅ **Added:** GitHub Pages support with `.nojekyll`
- ✅ **Updated:** All file paths to work with static hosting
- ✅ **Kept:** Original Flask setup in `flaskhost/` folder (for reference)

### If you need the Flask backend:

The original Flask implementation is still available in the `flaskhost/` directory:

```bash
pip install -r requirements.txt
cd flaskhost
python run.py
```

This is useful if you need:
- Custom server-side processing
- Advanced CORS configurations
- SharedArrayBuffer with specific headers

## 📜 License

[Add your license information here]

## 🙏 Credits

Built with:
- [Three.js](https://threejs.org/) - 3D rendering library
- [Gaussian Splats 3D](https://github.com/mkkellogg/GaussianSplats3D) - Gaussian splatting rendering
- GitHub Pages - Free static site hosting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
