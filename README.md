# beta-splatting-webviewer

A DBS web viewer built with Three.js and Flask.

## SharedArrayBuffer Support

This application uses SharedArrayBuffer for improved performance when transferring data between the main thread and web workers. However, SharedArrayBuffer requires cross-origin isolation to work properly.

### If you see a "SharedArrayBuffer transfer requires self.crossOriginIsolated" error:

The application will automatically fall back to regular memory transfer mode. To enable SharedArrayBuffer for better performance:

1. **For Flask development server**: Uncomment the cross-origin isolation headers in `flaskhost/app.py`:
   ```python
   @app.after_request
   def add_cross_origin_isolation_headers(response):
       response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
       response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
       return response
   ```

2. **For production servers**: Add these headers to your server configuration:
   - `Cross-Origin-Embedder-Policy: require-corp`
   - `Cross-Origin-Opener-Policy: same-origin`

3. **For local development**: You can also use `python -m http.server` with custom headers or browser flags for testing.

The application will work without these headers, but may have reduced performance for large splat scenes.

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Run the Flask server: `python flaskhost/run.py`
3. Open your browser to `http://localhost:8080`
