from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Validate file size"""
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    return file_size <= MAX_FILE_SIZE

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Job Application Webhook is running'
    }), 200

@app.route('/webhook/acbef742-9d51-4d52-bca0-c1bc5c9104b0', methods=['POST'])
def job_application_webhook():
    """
    Main webhook endpoint to receive job application data
    Expects:
    - resume: PDF file
    - title: Job title (required)
    - experience: Years of experience (required)
    - location: Job location (required)
    - github: GitHub URL (optional)
    - linkedin: LinkedIn URL (optional)
    """
    try:
        # Validate required form fields
        required_fields = ['title', 'experience', 'location']
        for field in required_fields:
            if field not in request.form:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'required_fields': required_fields
                }), 400

        # Extract form data
        title = request.form.get('title', '').strip()
        experience = request.form.get('experience', '').strip()
        location = request.form.get('location', '').strip()
        github = request.form.get('github', '').strip()
        linkedin = request.form.get('linkedin', '').strip()

        # Validate resume file
        if 'resume' not in request.files:
            return jsonify({
                'error': 'No resume file uploaded',
                'message': 'Please upload a PDF resume'
            }), 400

        resume_file = request.files['resume']

        if resume_file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a resume file'
            }), 400

        if not allowed_file(resume_file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'message': 'Only PDF files are allowed'
            }), 400

        if not validate_file_size(resume_file):
            return jsonify({
                'error': 'File too large',
                'message': f'Maximum file size is {MAX_FILE_SIZE / (1024 * 1024)}MB'
            }), 400

        # Read file content
        resume_content = resume_file.read()
        resume_filename = secure_filename(resume_file.filename)

        # Prepare response data (mimicking n8n webhook structure)
        response_data = {
            'success': True,
            'message': 'Job application received successfully',
            'data': {
                'body': {
                    'title': title,
                    'experience': experience,
                    'location': location,
                    'github': github,
                    'linkedin': linkedin
                },
                'resume': {
                    'filename': resume_filename,
                    'size': len(resume_content),
                    'mimetype': 'application/pdf'
                }
            }
        }

        # Here you would typically:
        # 1. Save the resume file temporarily or to cloud storage
        # 2. Trigger the next step in your workflow
        # 3. Process the data through your n8n workflow or equivalent
        
        # For now, return success response
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'message': f'Maximum file size is {MAX_FILE_SIZE / (1024 * 1024)}MB'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )