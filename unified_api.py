#!/usr/bin/env python3
"""
unified_api.py - Unified Flask API combining Career Roadmap, Career Chat, and Course Recommendations

This script consolidates three separate Flask applications into one unified API server.
All endpoints are accessible from a single port with proper namespacing.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from datetime import datetime
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# ============================================
# Import Module 1: Career Roadmap Generator
# ============================================
try:
    # Assuming career roadmap code is in 'roadmap_api.py'
    # You'll need to refactor the first code into a module with these functions:
    from roadmap_api import (
        CareerPathPlanner as RoadmapPlanner,
        allowed_file,
        UPLOAD_FOLDER
    )
    
    # Initialize roadmap planner
    roadmap_planner = RoadmapPlanner()
    ROADMAP_AVAILABLE = True
    
    # Ensure upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
except ImportError as e:
    print(f"⚠️  Warning: Could not import roadmap_api: {e}")
    ROADMAP_AVAILABLE = False

# ============================================
# Import Module 2: Career Counselor Chat
# ============================================
try:
    # Assuming career assistant code is in 'career_assistant.py'
    from career_assistant import (
        CareerCounselor,
        GEMINI_SDK_AVAILABLE,
        GEMINI_KEY
    )
    
    # Store active counselor sessions
    chat_sessions = {}
    CHAT_AVAILABLE = GEMINI_SDK_AVAILABLE and bool(GEMINI_KEY)
    
except ImportError as e:
    print(f"⚠️  Warning: Could not import career_assistant: {e}")
    CHAT_AVAILABLE = False

# ============================================
# Import Module 3: Course Recommender
# ============================================
try:
    # Assuming course recommender code is in 'course_recommender.py'
    from course_recommender import (
        model as course_model,
        embeddings as course_embeddings,
        df as course_df
    )
    RECOMMENDER_AVAILABLE = True
    
except ImportError as e:
    print(f"⚠️  Warning: Could not import course_recommender: {e}")
    RECOMMENDER_AVAILABLE = False

# ============================================
# Helper Functions
# ============================================

def error_response(message: str, status_code: int = 400):
    """Create standardized error response"""
    return jsonify({
        "status": "error",
        "message": message,
        "timestamp": datetime.now().isoformat()
    }), status_code

def success_response(data, message: str = "Success"):
    """Create standardized success response"""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }), 200

def get_or_create_chat_session(session_id: str):
    """Get existing chat session or create new one"""
    if session_id not in chat_sessions:
        chat_sessions[session_id] = CareerCounselor(session_id=session_id)
    return chat_sessions[session_id]

# ============================================
# Root & Health Endpoints
# ============================================

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        "service": "Unified Career Development API",
        "version": "1.0.0",
        "status": "running",
        "services": {
            "roadmap_generator": ROADMAP_AVAILABLE,
            "career_chat": CHAT_AVAILABLE,
            "course_recommender": RECOMMENDER_AVAILABLE
        },
        "endpoints": {
            "roadmap": {
                "POST /api/roadmap/generate": "Generate career roadmap",
                "POST /api/roadmap/upload-resume": "Upload and process resume",
                "POST /api/roadmap/generate-with-resume": "Generate roadmap with resume"
            },
            "chat": {
                "POST /api/chat/ask": "Chat with career counselor",
                "POST /api/chat/profile": "Update user profile",
                "GET /api/chat/profile": "Get user profile",
                "GET /api/chat/history": "Get chat history",
                "DELETE /api/chat/history": "Clear chat history",
                "GET /api/chat/advice/<topic>": "Get specific advice"
            },
            "courses": {
                "POST /api/courses/recommend": "Get course recommendations"
            },
            "general": {
                "GET /api/health": "Health check",
                "GET /": "API documentation"
            }
        },
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Unified health check endpoint"""
    return jsonify({
        "status": "healthy",
        "services": {
            "roadmap_generator": {
                "available": ROADMAP_AVAILABLE,
                "status": "operational" if ROADMAP_AVAILABLE else "unavailable"
            },
            "career_chat": {
                "available": CHAT_AVAILABLE,
                "status": "operational" if CHAT_AVAILABLE else "unavailable",
                "active_sessions": len(chat_sessions) if CHAT_AVAILABLE else 0
            },
            "course_recommender": {
                "available": RECOMMENDER_AVAILABLE,
                "status": "operational" if RECOMMENDER_AVAILABLE else "unavailable"
            }
        },
        "timestamp": datetime.now().isoformat()
    }), 200

# ============================================
# Module 1: Career Roadmap Endpoints
# ============================================

@app.route('/api/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generate career roadmap based on user data"""
    if not ROADMAP_AVAILABLE:
        return error_response("Roadmap service not available", 503)
    
    try:
        user_data = request.get_json()
        
        if not user_data:
            return error_response("No data provided")
        
        required_fields = ['desired_role']
        missing_fields = [f for f in required_fields if f not in user_data or not user_data[f]]
        
        if missing_fields:
            return error_response(f'Missing required fields: {", ".join(missing_fields)}')
        
        # Generate roadmap
        roadmap_text = roadmap_planner.generate_career_path(user_data)
        roadmap_structured = roadmap_planner.parse_roadmap_to_json(roadmap_text)
        
        # Save roadmap (optional)
        filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_')}.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("PERSONALIZED CAREER ROADMAP\n")
            f.write("="*80 + "\n\n")
            f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
            f.write(f"Duration: {user_data.get('roadmap_duration', '6 months')}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(roadmap_text)
        
        return success_response({
            'roadmap_text': roadmap_text,
            'roadmap_structured': roadmap_structured,
            'saved_file': filename,
            'user_profile': {
                'desired_role': user_data.get('desired_role', 'N/A'),
                'branch': user_data.get('branch', 'N/A'),
                'duration': user_data.get('roadmap_duration', '6 months')
            }
        }, "Career roadmap generated successfully")
        
    except Exception as e:
        app.logger.error(f"Error generating roadmap: {traceback.format_exc()}")
        return error_response(f"Error generating roadmap: {str(e)}", 500)

@app.route('/api/roadmap/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and process resume PDF"""
    if not ROADMAP_AVAILABLE:
        return error_response("Roadmap service not available", 503)
    
    try:
        if 'resume' not in request.files:
            return error_response('No resume file provided')
        
        file = request.files['resume']
        
        if file.filename == '':
            return error_response('No file selected')
        
        if not allowed_file(file.filename):
            return error_response('Only PDF files are allowed')
        
        resume_text = roadmap_planner.extract_text_from_pdf(file)
        
        if not resume_text:
            return error_response('Could not extract text from PDF')
        
        return success_response({
            'resume_content': resume_text,
            'filename': file.filename
        }, "Resume processed successfully")
        
    except Exception as e:
        app.logger.error(f"Error processing resume: {traceback.format_exc()}")
        return error_response(f"Error processing resume: {str(e)}", 500)

@app.route('/api/roadmap/generate-with-resume', methods=['POST'])
def generate_roadmap_with_resume():
    """Generate roadmap with resume upload in one request"""
    if not ROADMAP_AVAILABLE:
        return error_response("Roadmap service not available", 503)
    
    try:
        if 'resume' not in request.files:
            return error_response('No resume file provided')
        
        file = request.files['resume']
        
        if file.filename == '':
            return error_response('No file selected')
        
        if not allowed_file(file.filename):
            return error_response('Only PDF files are allowed')
        
        resume_text = roadmap_planner.extract_text_from_pdf(file)
        
        if not resume_text:
            return error_response('Could not extract text from PDF')
        
        import json
        user_data_str = request.form.get('data')
        if not user_data_str:
            return error_response('No user data provided')
        
        user_data = json.loads(user_data_str)
        user_data['resume_content'] = resume_text
        
        # Generate roadmap
        roadmap_text = roadmap_planner.generate_career_path(user_data)
        roadmap_structured = roadmap_planner.parse_roadmap_to_json(roadmap_text)
        
        return success_response({
            'roadmap_text': roadmap_text,
            'roadmap_structured': roadmap_structured,
            'resume_processed': True
        }, "Resume processed and roadmap generated successfully")
        
    except Exception as e:
        app.logger.error(f"Error: {traceback.format_exc()}")
        return error_response(f"Error processing request: {str(e)}", 500)

# ============================================
# Module 2: Career Chat Endpoints
# ============================================

@app.route('/api/chat/ask', methods=['POST'])
def chat_ask():
    """Chat with career counselor"""
    if not CHAT_AVAILABLE:
        return error_response("Chat service not available. Please configure GEMINI_API_KEY", 503)
    
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON")
        
        query = data.get('query', '').strip()
        session_id = data.get('session_id', f"session_{int(datetime.now().timestamp() * 1000)}")
        include_history = data.get('include_history', True)
        
        if not query:
            return error_response("Query parameter is required")
        
        counselor = get_or_create_chat_session(session_id)
        result = counselor.ask(query, include_history=include_history)
        
        if result['status'] == 'success':
            return success_response(result, "Response generated successfully")
        else:
            return error_response(result.get('response', 'Unknown error'), 500)
            
    except Exception as e:
        app.logger.error(f"Error in chat: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/chat/profile', methods=['POST'])
def update_chat_profile():
    """Update user profile for chat"""
    if not CHAT_AVAILABLE:
        return error_response("Chat service not available", 503)
    
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON")
        
        session_id = data.get('session_id')
        profile_data = data.get('profile', {})
        
        if not session_id:
            return error_response("session_id is required")
        
        counselor = get_or_create_chat_session(session_id)
        result = counselor.update_user_profile(profile_data)
        
        if result['status'] == 'success':
            return success_response(result, "Profile updated successfully")
        else:
            return error_response(result.get('message', 'Failed to update profile'), 400)
            
    except Exception as e:
        app.logger.error(f"Error updating profile: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/chat/profile', methods=['GET'])
def get_chat_profile():
    """Get user profile"""
    if not CHAT_AVAILABLE:
        return error_response("Chat service not available", 503)
    
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return error_response("session_id query parameter is required")
        
        counselor = get_or_create_chat_session(session_id)
        profile = counselor.get_user_profile()
        
        return success_response({
            "session_id": session_id,
            "profile": profile
        }, "Profile retrieved successfully")
        
    except Exception as e:
        app.logger.error(f"Error getting profile: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get conversation history"""
    if not CHAT_AVAILABLE:
        return error_response("Chat service not available", 503)
    
    try:
        session_id = request.args.get('session_id')
        limit = request.args.get('limit', type=int)
        
        if not session_id:
            return error_response("session_id query parameter is required")
        
        counselor = get_or_create_chat_session(session_id)
        history = counselor.get_conversation_history(limit=limit)
        
        return success_response({
            "session_id": session_id,
            "message_count": len(history),
            "history": history
        }, "History retrieved successfully")
        
    except Exception as e:
        app.logger.error(f"Error getting history: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/chat/history', methods=['DELETE'])
def clear_chat_history():
    """Clear conversation history"""
    if not CHAT_AVAILABLE:
        return error_response("Chat service not available", 503)
    
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON")
        
        session_id = data.get('session_id')
        
        if not session_id:
            return error_response("session_id is required")
        
        counselor = get_or_create_chat_session(session_id)
        result = counselor.clear_history()
        
        if result['status'] == 'success':
            return success_response({"session_id": session_id}, "History cleared successfully")
        else:
            return error_response(result.get('message', 'Failed to clear history'), 400)
            
    except Exception as e:
        app.logger.error(f"Error clearing history: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/chat/advice/<topic>', methods=['GET'])
def get_career_advice(topic: str):
    """Get specific career advice on a topic"""
    if not CHAT_AVAILABLE:
        return error_response("Chat service not available", 503)
    
    try:
        session_id = request.args.get('session_id', f"advice_{int(datetime.now().timestamp() * 1000)}")
        
        counselor = get_or_create_chat_session(session_id)
        result = counselor.get_career_advice(topic)
        
        if result['status'] == 'success':
            return success_response({
                "topic": topic,
                "response": result['response'],
                "session_id": result['session_id']
            }, f"Advice for '{topic}' retrieved successfully")
        else:
            return error_response(result.get('response', 'Failed to get advice'), 500)
            
    except Exception as e:
        app.logger.error(f"Error getting advice: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

# ============================================
# Module 3: Course Recommender Endpoints
# ============================================

@app.route('/api/courses/recommend', methods=['POST'])
def recommend_courses():
    """Get course recommendations based on query"""
    if not RECOMMENDER_AVAILABLE:
        return error_response("Course recommender service not available", 503)
    
    try:
        from sentence_transformers import util
        import torch
        
        data = request.get_json()
        user_input = data.get("query", "")
        top_k = data.get("top_k", 3)  # Allow customizable number of results
        
        if not user_input.strip():
            return error_response("Empty input query")
        
        # Encode user input
        user_embedding = course_model.encode([user_input], convert_to_tensor=True)
        
        # Compute cosine similarity
        cosine_scores = util.cos_sim(user_embedding, course_embeddings)[0]
        
        # Get top results
        top_results = torch.topk(cosine_scores, k=min(top_k, len(cosine_scores)))
        
        # Prepare response
        recommendations = []
        for idx, score in zip(top_results[1], top_results[0]):
            i = int(idx)
            recommendations.append({
                "course_title": course_df.iloc[i]['course_title'],
                "organization": course_df.iloc[i]['course_organization'],
                "skills": course_df.iloc[i]['course_skills'],
                "url": course_df.iloc[i]['course_url'],
                "similarity_score": round(float(score), 4)
            })
        
        return success_response({
            "query": user_input,
            "total_recommendations": len(recommendations),
            "top_courses": recommendations
        }, "Course recommendations generated successfully")
        
    except Exception as e:
        app.logger.error(f"Error recommending courses: {traceback.format_exc()}")
        return error_response(f"Error generating recommendations: {str(e)}", 500)

# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def not_found(e):
    return error_response("Endpoint not found", 404)

@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("Method not allowed for this endpoint", 405)

@app.errorhandler(413)
def request_entity_too_large(e):
    return error_response("File too large. Maximum size is 16MB", 413)

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Internal server error: {traceback.format_exc()}")
    return error_response("Internal server error", 500)

# ============================================
# Main Entry Point
# ============================================

def main():
    """Run the unified Flask application"""
    print("\n" + "="*80)
    print("UNIFIED CAREER DEVELOPMENT API SERVER".center(80))
    print("="*80 + "\n")
    
    # Check service availability
    print("📊 Service Status:")
    print(f"  • Career Roadmap Generator: {'✅ Available' if ROADMAP_AVAILABLE else '❌ Unavailable'}")
    print(f"  • Career Chat Counselor:    {'✅ Available' if CHAT_AVAILABLE else '❌ Unavailable'}")
    print(f"  • Course Recommender:       {'✅ Available' if RECOMMENDER_AVAILABLE else '❌ Unavailable'}")
    print()
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting unified server on http://{host}:{port}")
    print()
    print("📡 Available API Endpoints:")
    print()
    
    if ROADMAP_AVAILABLE:
        print("  [ROADMAP SERVICE]")
        print(f"    • POST   /api/roadmap/generate")
        print(f"    • POST   /api/roadmap/upload-resume")
        print(f"    • POST   /api/roadmap/generate-with-resume")
        print()
    
    if CHAT_AVAILABLE:
        print("  [CHAT SERVICE]")
        print(f"    • POST   /api/chat/ask")
        print(f"    • POST   /api/chat/profile")
        print(f"    • GET    /api/chat/profile?session_id=<id>")
        print(f"    • GET    /api/chat/history?session_id=<id>")
        print(f"    • DELETE /api/chat/history")
        print(f"    • GET    /api/chat/advice/<topic>")
        print()
    
    if RECOMMENDER_AVAILABLE:
        print("  [COURSE RECOMMENDER SERVICE]")
        print(f"    • POST   /api/courses/recommend")
        print()
    
    print("  [GENERAL]")
    print(f"    • GET    /api/health")
    print(f"    • GET    /")
    print()
    print("📚 Full API documentation at: http://{host}:{port}/")
    print()
    print("Press CTRL+C to stop the server")
    print("="*80 + "\n")
    
    # Run the app
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
