from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
from api.routes import api_bp

# Load environment variables from the backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# More verbose environment variable loading
try:
    # First try to load from the specific path
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
        print(f"Loaded environment from: {ENV_PATH}", file=sys.stderr)
    else:
        print(f"Warning: .env file not found at {ENV_PATH}", file=sys.stderr)
        # Try to load from current directory as fallback
        load_dotenv()
        print("Attempted to load .env from current directory", file=sys.stderr)
    
    # Check if GEMINI_API_KEY is loaded
    if 'GEMINI_API_KEY' in os.environ:
        # Don't print the actual key for security reasons
        print("GEMINI_API_KEY is set in environment", file=sys.stderr)
    else:
        print("WARNING: GEMINI_API_KEY is not set in environment", file=sys.stderr)
        print("Current environment variables:", file=sys.stderr)
        for key, value in os.environ.items():
            if 'API' in key or 'KEY' in key:
                print(f"  {key}: {'*' * len(value) if value else 'not set'}", file=sys.stderr)
    
except Exception as e:
    print(f"Error loading environment variables: {str(e)}", file=sys.stderr)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    
    # Configure app
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    app.config['TEMP_FOLDER'] = os.path.join(BASE_DIR, 'temp')
    app.config['MAX_CONTENT_LENGTH'] = 700 * 1024 * 1024  # Max 300MB uploads
    
    # Ensure upload and temp directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
    
    # Enable CORS with specific configuration
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Serve React app at root
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    # Handle React routing
    @app.route('/<path:path>')
    def catch_all(path):
        return app.send_static_file('index.html')
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': 'File is too large. Max size is 300MB.'}), 413
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)