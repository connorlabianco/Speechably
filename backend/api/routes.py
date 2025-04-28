from flask import Blueprint, request, jsonify, current_app
import os
import uuid
import tempfile
from werkzeug.utils import secure_filename
import json
import sys
from dotenv import load_dotenv

from services.audio_service import AudioSegmenter, AudioSegmenterConfig
from services.speech_analysis import SpeechAnalyzer
from services.transcription import TranscriptionService
from services.gemini_service import GeminiService
from utils.data_processor import DataProcessor
from utils.visualization import VisualizationHelper

# Create blueprint
api_bp = Blueprint('api', __name__)

# Get Gemini API key from environment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables", file=sys.stderr)
    print("Environment variables:", {k: v for k, v in os.environ.items() if 'API' in k or 'KEY' in k}, file=sys.stderr)
    # Try to load from .env file directly as a fallback
    load_dotenv()
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if GEMINI_API_KEY:
        print("Successfully loaded GEMINI_API_KEY from .env file", file=sys.stderr)
    else:
        print("Failed to load GEMINI_API_KEY from both environment and .env file", file=sys.stderr)

# Initialize services
speech_analyzer = SpeechAnalyzer()
transcription_service = TranscriptionService()
gemini_service = GeminiService(api_key=GEMINI_API_KEY)  # Pass API key explicitly
visualization_helper = VisualizationHelper()

# Configure audio segmenter - use system FFmpeg path or default
FFMPEG_PATH = os.environ.get('FFMPEG_PATH', 'ffmpeg')
audio_config = AudioSegmenterConfig(ffmpeg_path=FFMPEG_PATH)
audio_segmenter = AudioSegmenter(audio_config)
data_processor = DataProcessor(FFMPEG_PATH)

def allowed_file(filename):
    """Check if file has an allowed extension"""
    ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'webm'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/upload', methods=['POST'])
def upload_video():
    """
    Handle video upload and processing
    Returns analysis results including emotion segments and transcription
    """
    # Check if file part exists
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Create a unique filename
    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    unique_filename = f"{unique_id}_{filename}"
    
    # Save uploaded file
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(upload_path)
    
    # Create a temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Create output directory for segments
            output_dir = os.path.join(temp_dir, "output_segments")
            os.makedirs(output_dir, exist_ok=True)
            
            # Extract and split audio
            full_audio_path, segment_paths = audio_segmenter.extract_and_split_audio(upload_path, output_dir)
            
            # Get total duration of the full audio
            total_duration = data_processor.get_audio_duration(full_audio_path)
            
            # Analyze the segments for emotions
            results = speech_analyzer.analyze_segments(output_dir)
            
            # Get segment durations
            segment_durations = [data_processor.get_audio_duration(path) for path in segment_paths]
            
            # Process emotion data into time-based segments
            emotion_segments = data_processor.process_emotion_data(
                results, 
                total_duration, 
                segment_durations
            )
            
            # Calculate average segment duration (for WPS)
            average_segment_duration = total_duration / len(segment_paths) if segment_paths else 0
            
            # Transcribe segments
            transcription_data = transcription_service.transcribe_segments(
                segment_paths, 
                average_segment_duration,
                emotion_data=emotion_segments
            )
            
            # Generate LLM insights
            gemini_analysis = gemini_service.analyze_speech(emotion_segments, transcription_data)
            
            # Log the analysis result (for debugging)
            print(f"Gemini analysis summary: {gemini_analysis.get('summary', 'Not available')[:100]}...", file=sys.stderr)
            
            # Save all analysis results to a file
            results_path = data_processor.save_analysis_results(
                output_dir, 
                emotion_segments, 
                transcription_data,
                gemini_analysis
            )
            
            # Prepare visualization data
            emotion_df = visualization_helper.prepare_emotion_timeline_data(emotion_segments)
            emotion_metrics = visualization_helper.calculate_emotion_metrics(emotion_df)
            wps_data = None
            speech_clarity = None
            
            if transcription_data:
                wps_data = visualization_helper.prepare_wps_data(transcription_data)
                speech_clarity = visualization_helper.prepare_speech_clarity_data(transcription_data)
            
            # Create response data
            response_data = {
                'success': True,
                'video_id': unique_id,
                'emotion_segments': [{'time_range': tr, 'emotion': e} for tr, e in emotion_segments],
                'transcription_data': transcription_data,
                'gemini_analysis': gemini_analysis,
                'emotion_metrics': emotion_metrics,
                'speech_clarity': speech_clarity if transcription_data else None,
                'wps_data': json.loads(wps_data.to_json(orient='records')) if wps_data is not None else None,
                'duration': total_duration
            }
            
            return jsonify(response_data), 200
            
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stderr)
            return jsonify({'error': str(e)}), 500
        
        finally:
            # Clean up the uploaded file if needed
            # Uncomment to delete after processing:
            if os.path.exists(upload_path):
                os.remove(upload_path)
            pass

@api_bp.route('/chat', methods=['POST'])
def chat_with_coach():
    """Handle chat requests to the AI coach"""
    try:
        data = request.json
        user_input = data.get('message', '')
        emotion_segments = data.get('emotion_segments', [])
        
        # Format emotion context for Gemini
        emotion_context = "\n".join([f"{seg['time_range']}: {seg['emotion']}" 
                                    for seg in emotion_segments])
        
        # Generate response
        response = gemini_service.generate_chat_response(user_input, emotion_context)
        
        return jsonify({'response': response}), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@api_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Simple health check endpoint"""
    # Also check Gemini service status
    gemini_status = "available" if gemini_service.model is not None else "unavailable"
    return jsonify({
        'status': 'ok',
        'services': {
            'gemini': gemini_status
        }
    }), 200