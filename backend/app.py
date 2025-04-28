from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api.routes import api_bp

# Load environment variables from the backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    
    # Configure app
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    app.config['TEMP_FOLDER'] = os.path.join(BASE_DIR, 'temp')
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Max 500MB uploads
    
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
        return jsonify({'error': 'File is too large. Max size is 500MB.'}), 413
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)