#!/usr/bin/env python3
"""
Simple startup script for the Beta Flask server.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Beta Flask Server")
    print("=" * 60)
    print("Starting server...")
    print("Serving files from:", Path(__file__).parent.parent)
    print("Open your browser to: http://localhost:8080")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1) 