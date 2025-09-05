from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Enable cross-origin isolation headers for SharedArrayBuffer support
# Uncomment these lines if you want to enable SharedArrayBuffer for better performance
@app.after_request
def add_cross_origin_isolation_headers(response):
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    return response

# Get the web directory to serve static files
PARENT_DIR = Path(__file__).parent.parent
WEB_DIR = PARENT_DIR / "web"
ASSETS_DIR = WEB_DIR / "assets"

@app.route('/')
def index():
    """Serve the main 3D Gaussian Splat application page from web directory"""
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/three.module.js')
def three_js():
    """Serve the Three.js module from web directory"""
    return send_from_directory(WEB_DIR, 'three.module.js', mimetype='application/javascript')

@app.route('/gaussian-splats-3d.module.js')
def gaussian_splats_js():
    """Serve the Gaussian Splats 3D module from web directory"""
    return send_from_directory(WEB_DIR, 'gaussian-splats-3d.module.js', mimetype='application/javascript')

@app.route('/assets/<path:filename>')
def assets(filename):
    """Serve asset files (PLY files, etc.) from web/assets directory"""
    # Set appropriate MIME type for PLY files
    if filename.endswith('.ply'):
        mimetype = 'application/octet-stream'
    else:
        mimetype = None
    
    response = send_from_directory(ASSETS_DIR, filename, mimetype=mimetype)
    
    # Add CORS headers explicitly for asset files
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    return response

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "3D Gaussian Splat server is running"})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    print("Starting 3D Gaussian Splat Flask Server...")
    print(f"Web directory: {WEB_DIR}")
    print(f"Assets directory: {ASSETS_DIR}")
    print("Server will be available at: http://localhost:8080")
    
    app.run(host='0.0.0.0', port=8080, debug=True) 