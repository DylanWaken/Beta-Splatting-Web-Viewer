# beta-splatting-webviewer

A DBS (Dynamic Beta Splatting) web viewer built with Three.js and Flask.

![webview](/assets/webview.png)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Beta-Splatting-Web-Viewer
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

### Quick Start

1. **Start the Flask server:**
   ```bash
   cd flaskhost
   python run.py
   ```
   
   Or alternatively:
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:8080`

3. **View the visualization:**
   The viewer will automatically load and display the default Beta Splatting scene.

### Adding Your Own PLY Files

1. **For Beta Splatting (DBS) files:**
   - Place your PLY file in `web/assets/bs/`
   - Update the path in `web/betaindex.html`:
     ```javascript
     let path = 'assets/bs/your_file.ply';
     ```

2. **For standard Gaussian Splatting files:**
   - Place your PLY file in `web/assets/gs/`
   - The standard viewer is available at `web/index.html`

### Customization

#### Camera Settings

Modify camera parameters in `web/betaindex.html`:

```javascript
const viewer = new BetaView.Viewer({
    'cameraUp': [0, 0, 1],              // Camera up vector
    'initialCameraPosition': [0, 1, 0], // Starting position
    'initialCameraLookAt': [1, 0, 0],   // Look at point
});
```

#### Server Configuration

Modify server settings in `flaskhost/app.py`:

- **Port:** Change the port number (default: 8080)
  ```python
  app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
  ```

- **CORS Settings:** Adjust CORS headers for cross-origin requests
- **Shared Array Buffer:** Enabled by default for better performance

### Controls

- **Left Mouse Button:** Rotate camera
- **Right Mouse Button:** Pan camera
- **Mouse Wheel:** Zoom in/out
- **Touch Gestures:** Supported on mobile devices

## Project Structure

```
Beta-Splatting-Web-Viewer/
├── flaskhost/              # Flask backend server
│   ├── app.py             # Main Flask application
│   ├── run.py             # Server startup script
│   └── templates/         # HTML templates
├── web/                   # Frontend web viewer
│   ├── betaindex.html     # Beta Splatting viewer entry point
│   ├── betaview.js        # Beta Splatting viewer module
│   ├── betaviewSB.js      # Beta Splatting with SharedBuffer
│   ├── three.module.js    # Three.js library
│   └── assets/            # PLY files and assets
│       ├── bs/            # Beta Splatting files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### Server won't start
- Check if port 8080 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're running from the `flaskhost` directory

### PLY file not loading
- Verify the file path in the HTML file matches your PLY location
- Check browser console (F12) for error messages
- Ensure the PLY file is in the correct format
- Verify CORS headers are properly configured

### Performance issues
- Ensure SharedArrayBuffer support is enabled (requires HTTPS or localhost)
- Try reducing the size of the PLY file
- Use the streaming view option: `'streamView': true`
- Close other browser tabs consuming resources

### Browser compatibility
- Use the latest version of Chrome, Firefox, Edge, or Safari
- Enable WebGL in your browser settings
- Check if hardware acceleration is enabled

## Development

To modify the viewer behavior:

1. **Edit viewer settings:** Modify `web/betaindex.html`
2. **Update server routes:** Edit `flaskhost/app.py`
3. **Add new features:** Extend `web/betaview.js` or `web/betaviewSB.js`

For development with auto-reload, Flask debug mode is enabled by default.

## Health Check

The server includes a health check endpoint:
```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "message": "3D Gaussian Splat server is running"
}
```

## License

[Add your license information here]

## Credits

Built with:
- [Three.js](https://threejs.org/) - 3D rendering library
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [Gaussian Splats 3D](https://github.com/mkkellogg/GaussianSplats3D) - Gaussian splatting rendering

