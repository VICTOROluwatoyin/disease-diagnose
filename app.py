import os
import io
import base64
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import google.generativeai as genai
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_image(image_path, max_size=(800, 800), quality=85):
    """Compress image to reduce file size while maintaining quality"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save compressed image
            compressed_path = image_path.replace('.', '_compressed.')
            img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
            return compressed_path
    except Exception as e:
        print(f"Error compressing image: {e}")
        return image_path

def analyze_symptom_image(image_path):
    """Analyze medical symptom from image using Gemini API"""
    try:
        # Compress image first
        compressed_path = compress_image(image_path)
        
        # Read and prepare image
        with open(compressed_path, 'rb') as img_file:
            image_data = img_file.read()
        
        # Create the image part for Gemini
        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_data).decode()
        }
        
        # Medical analysis prompt
        prompt = """
        You are a medical AI assistant. Analyze this image and provide a detailed assessment of any visible symptoms, conditions, or abnormalities. 

        Please provide:
        1. **Visual Observations**: Describe what you see in the image
        2. **Possible Conditions**: List potential medical conditions that could cause these symptoms
        3. **Severity Assessment**: Rate the urgency (Low, Moderate, High, Emergency)
        4. **Recommendations**: Suggest next steps or when to seek medical care
        5. **Additional Information**: Any relevant details about the condition

        IMPORTANT DISCLAIMERS:
        - This is not a medical diagnosis
        - Always consult healthcare professionals for proper diagnosis
        - Seek immediate medical attention for severe symptoms
        - This analysis is for informational purposes only

        Format your response in a clear, structured way with appropriate medical terminology explained in simple terms.
        """
        
        # Generate response
        response = model.generate_content([prompt, image_part])
        
        # Clean up compressed file
        if compressed_path != image_path and os.path.exists(compressed_path):
            os.remove(compressed_path)
        
        return {
            'success': True,
            'analysis': response.text,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Analyze the image
            analysis_result = analyze_symptom_image(filepath)
            
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return jsonify(analysis_result)
            
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/analyze_live', methods=['POST'])
def analyze_live():
    """Handle live capture (camera/screen) analysis"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Extract base64 image data
        image_data = data['image']
        capture_type = data.get('type', 'unknown')
        
        # Remove data URL prefix if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Validate base64 data
        if not image_data or len(image_data) < 100:
            return jsonify({'error': 'Invalid or empty image data'}), 400
        
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data)
            if len(image_bytes) < 1000:  # Minimum reasonable image size
                return jsonify({'error': 'Image data too small'}), 400
        except Exception as e:
            print(f"Base64 decode error: {e}")
            return jsonify({'error': 'Invalid image data format'}), 400
        
        # Save temporary file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"live_capture_{capture_type}_{timestamp}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            # Verify the file was created and has content
            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                return jsonify({'error': 'Failed to save captured image'}), 500
            
            print(f"Saved live capture: {filepath} ({len(image_bytes)} bytes)")
            
        except Exception as e:
            print(f"File save error: {e}")
            return jsonify({'error': f'Failed to save image: {str(e)}'}), 500
        
        # Analyze the image
        analysis_result = analyze_symptom_image(filepath)
        
        # Clean up temporary file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify(analysis_result)
        
    except Exception as e:
        print(f"Live analysis error: {e}")
        return jsonify({'error': f'Error processing live capture: {str(e)}'}), 500

@app.route('/about')
def about():
    """About page with medical disclaimers"""
    return render_template('about.html')

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Get host and port from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host=host, port=port) 