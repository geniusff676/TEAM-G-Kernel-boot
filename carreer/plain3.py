# # from flask import Flask, request, jsonify
# # import os
# # from werkzeug.utils import secure_filename

# # app = Flask(__name__)

# # # Configuration
# # UPLOAD_FOLDER = 'uploads'
# # ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
# # MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# # # Create upload folder if it doesn't exist
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# # def allowed_file(filename):
# #     return '.' in filename and \
# #            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # @app.route('/upload-resume', methods=['POST'])
# # def upload_resume():
# #     try:
# #         # Get all form data
# #         form_data = request.form.to_dict()
        
# #         # Get all files
# #         files_data = {}
        
# #         # Iterate through all files in the request
# #         for field_name in request.files:
# #             file = request.files[field_name]
            
# #             if file and file.filename:
# #                 # Secure the filename
# #                 filename = secure_filename(file.filename)
                
# #                 # Save the file
# #                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #                 file.save(filepath)
                
# #                 files_data[field_name] = {
# #                     'filename': filename,
# #                     'original_name': file.filename,
# #                     'content_type': file.content_type,
# #                     'saved_path': filepath
# #                 }
        
# #         # Get headers (optional)
# #         headers = dict(request.headers)
        
# #         # Get query parameters (optional)
# #         query_params = request.args.to_dict()
        
# #         response = {
# #             'status': 'success',
# #             'message': 'Resume uploaded successfully',
# #             'form_data': form_data,
# #             'files': files_data,
# #             'query_params': query_params
# #         }
        
# #         return jsonify(response), 200
        
# #     except Exception as e:
# #         return jsonify({
# #             'status': 'error',
# #             'message': str(e)
# #         }), 400


# # @app.route('/health', methods=['GET'])
# # def health_check():
# #     return jsonify({'status': 'ok'}), 200


# # if __name__ == '__main__':
# #     app.run(debug=True, host='0.0.0.0', port=5003)

# from flask import Flask, request, jsonify, send_file
# import os
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/upload-resume', methods=['POST'])
# def upload_resume():
#     try:
#         # Get form data
#         form_data = request.form.to_dict()
        
#         # Debug: Print all files received
#         print("Files received:", request.files.keys())
#         print("Form data received:", form_data)
        
#         # Try to get the file with different possible field names
#         file = None
#         for key in request.files.keys():
#             file = request.files[key]
#             break
        
#         # Also try specific field name
#         if not file:
#             file = request.files.get('updatedResume') or \
#                    request.files.get('file') or \
#                    request.files.get('data')
        
#         if not file or file.filename == '':
#             return jsonify({
#                 'status': 'error', 
#                 'message': 'No file uploaded',
#                 'received_fields': list(request.files.keys()),
#                 'form_data': form_data
#             }), 400
        
#         # Save the file temporarily
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
        
#         # Get the resume title from form data
#         resume_title = form_data.get('filename', filename)
        
#         # Return the file directly as binary with metadata in headers
#         response = send_file(
#             filepath,
#             mimetype=file.content_type or 'text/plain',
#             as_attachment=True,
#             download_name=f"{resume_title}"
#         )
        
#         # Add custom headers with metadata
#         response.headers['X-Original-Filename'] = file.filename
#         response.headers['X-Resume-Title'] = resume_title
        
#         return response
        
#     except Exception as e:
#         import traceback
#         return jsonify({
#             'status': 'error', 
#             'message': str(e),
#             'traceback': traceback.format_exc()
#         }), 400


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5003)
from flask import Flask, request, jsonify, send_file
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
RECORDS_FILE = os.path.join(DATA_FOLDER, 'upload_records.json')

# Create necessary folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def load_records():
    """Load all upload records from JSON file"""
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_records(records):
    """Save all upload records to JSON file"""
    with open(RECORDS_FILE, 'w') as f:
        json.dump(records, indent=2, fp=f)


@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    try:
        # Generate unique ID for this upload
        upload_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Get form data (INPUT)
        form_data = request.form.to_dict()
        
        # Get the file
        file = None
        file_field_name = None
        for key in request.files.keys():
            file = request.files[key]
            file_field_name = key
            break
        
        if not file or file.filename == '':
            return jsonify({
                'status': 'error', 
                'message': 'No file uploaded',
                'upload_id': upload_id,
                'timestamp': timestamp
            }), 400
        
        # Save the file with unique name
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{upload_id}{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        
        # Prepare INPUT data
        input_data = {
            'form_data': form_data,
            'original_filename': original_filename,
            'file_field_name': file_field_name,
            'content_type': file.content_type,
            'resume_title': form_data.get('filename', original_filename)
        }
        
        # Prepare OUTPUT data
        output_data = {
            'upload_id': upload_id,
            'saved_filename': unique_filename,
            'file_path': filepath,
            'file_size': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'status': 'success',
            'message': 'Resume uploaded successfully'
        }
        
        # Create complete record
        upload_record = {
            'upload_id': upload_id,
            'timestamp': timestamp,
            'input': input_data,
            'output': output_data,
            'status': 'completed'
        }
        
        # Load existing records, add new one, and save
        records = load_records()
        records.append(upload_record)
        save_records(records)
        
        # Return JSON response
        response = {
            'status': 'success',
            'message': 'Resume uploaded and data stored successfully',
            'upload_id': upload_id,
            'timestamp': timestamp,
            'data': upload_record
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        
        # Store error record
        error_record = {
            'upload_id': upload_id if 'upload_id' in locals() else str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'input': {
                'form_data': request.form.to_dict() if request.form else {},
                'files_received': list(request.files.keys())
            },
            'output': {
                'status': 'error',
                'message': str(e),
                'traceback': traceback.format_exc()
            },
            'status': 'failed'
        }
        
        records = load_records()
        records.append(error_record)
        save_records(records)
        
        return jsonify({
            'status': 'error', 
            'message': str(e),
            'upload_id': error_record['upload_id'],
            'timestamp': error_record['timestamp']
        }), 400


@app.route('/records', methods=['GET'])
def get_all_records():
    """Get all upload records"""
    try:
        records = load_records()
        return jsonify({
            'status': 'success',
            'count': len(records),
            'records': records
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/record/<upload_id>', methods=['GET'])
def get_record(upload_id):
    """Get a specific upload record by ID"""
    try:
        records = load_records()
        record = next((r for r in records if r['upload_id'] == upload_id), None)
        
        if record:
            return jsonify({
                'status': 'success',
                'record': record
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Record not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/download/<upload_id>', methods=['GET'])
def download_file(upload_id):
    """Download the uploaded file by upload ID"""
    try:
        records = load_records()
        record = next((r for r in records if r['upload_id'] == upload_id), None)
        
        if not record:
            return jsonify({
                'status': 'error',
                'message': 'Record not found'
            }), 404
        
        filepath = record['output']['file_path']
        original_filename = record['input']['original_filename']
        
        if not os.path.exists(filepath):
            return jsonify({
                'status': 'error',
                'message': 'File not found on server'
            }), 404
        
        return send_file(
            filepath,
            mimetype=record['input']['content_type'] or 'application/octet-stream',
            as_attachment=True,
            download_name=original_filename
        )
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about uploads"""
    try:
        records = load_records()
        
        total_uploads = len(records)
        successful_uploads = len([r for r in records if r['status'] == 'completed'])
        failed_uploads = len([r for r in records if r['status'] == 'failed'])
        
        total_size = sum([
            r['output'].get('file_size', 0) 
            for r in records 
            if r['status'] == 'completed'
        ])
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_uploads': total_uploads,
                'successful_uploads': successful_uploads,
                'failed_uploads': failed_uploads,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
    