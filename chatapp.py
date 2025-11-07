#!/usr/bin/env python3
"""
app.py - Flask API for AI Career Counselor
Provides REST endpoints to interact with the career counseling assistant.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import os
import traceback
from datetime import datetime
from typing import Dict, Any

# Import the career assistant module
from career_assistant import CareerCounselor, GEMINI_SDK_AVAILABLE, GEMINI_KEY

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Store active counselor sessions in memory
# In production, use Redis or database
sessions: Dict[str, CareerCounselor] = {}

# -----------------------------
# Helper Functions
# -----------------------------
def get_or_create_session(session_id: str) -> CareerCounselor:
    """Get existing session or create new one"""
    if session_id not in sessions:
        sessions[session_id] = CareerCounselor(session_id=session_id)
    return sessions[session_id]

def error_response(message: str, status_code: int = 400) -> tuple:
    """Create standardized error response"""
    return jsonify({
        "status": "error",
        "message": message,
        "timestamp": datetime.now().isoformat()
    }), status_code

def success_response(data: Any, message: str = "Success") -> tuple:
    """Create standardized success response"""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }), 200

# -----------------------------
# Middleware/Decorators
# -----------------------------
def require_gemini(f):
    """Decorator to check if Gemini SDK is available"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not GEMINI_SDK_AVAILABLE:
            return error_response(
                "Gemini SDK not available. Please install google-genai package.",
                503
            )
        if not GEMINI_KEY:
            return error_response(
                "GEMINI_API_KEY not configured. Please set your API key.",
                503
            )
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------
# API Endpoints
# -----------------------------

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        "service": "AI Career Counselor API",
        "version": "1.0.0",
        "status": "running",
        "gemini_available": GEMINI_SDK_AVAILABLE,
        "api_configured": bool(GEMINI_KEY),
        "endpoints": {
            "POST /api/chat": "Send a query and get career advice",
            "POST /api/profile": "Update user profile",
            "GET /api/profile": "Get user profile",
            "GET /api/history": "Get conversation history",
            "DELETE /api/history": "Clear conversation history",
            "GET /api/advice/<topic>": "Get specific career advice",
            "GET /api/health": "Health check endpoint",
            "GET /api/topics": "Get available advice topics"
        },
        "documentation": "Use POST /api/chat with JSON body: {session_id, query}",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "gemini_sdk": GEMINI_SDK_AVAILABLE,
        "api_key_set": bool(GEMINI_KEY),
        "active_sessions": len(sessions),
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/chat', methods=['POST'])
@require_gemini
def chat():
    """
    Main chat endpoint for career counseling
    
    Request JSON:
    {
        "session_id": "optional-session-id",
        "query": "Your career question",
        "include_history": true (optional, default: true)
    }
    
    Response:
    {
        "status": "success",
        "data": {
            "response": "Career counselor response",
            "session_id": "session-id",
            "timestamp": "ISO timestamp"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON")
        
        # Extract parameters
        query = data.get('query', '').strip()
        session_id = data.get('session_id', f"session_{int(datetime.now().timestamp() * 1000)}")
        include_history = data.get('include_history', True)
        
        if not query:
            return error_response("Query parameter is required and cannot be empty")
        
        # Get or create session
        counselor = get_or_create_session(session_id)
        
        # Get response
        result = counselor.ask(query, include_history=include_history)
        
        if result['status'] == 'success':
            return success_response(result, "Response generated successfully")
        else:
            return error_response(result.get('response', 'Unknown error'), 500)
            
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/profile', methods=['POST'])
@require_gemini
def update_profile():
    """
    Update user profile
    
    Request JSON:
    {
        "session_id": "session-id",
        "profile": {
            "education": "Bachelor's in Computer Science",
            "experience": "3 years",
            "skills": ["Python", "JavaScript", "React"],
            "interests": ["Web Development", "AI/ML"],
            "goals": "Become a senior developer"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON")
        
        session_id = data.get('session_id')
        profile_data = data.get('profile', {})
        
        if not session_id:
            return error_response("session_id is required")
        
        if not profile_data:
            return error_response("profile data is required")
        
        # Get or create session
        counselor = get_or_create_session(session_id)
        
        # Update profile
        result = counselor.update_user_profile(profile_data)
        
        if result['status'] == 'success':
            return success_response(result, "Profile updated successfully")
        else:
            return error_response(result.get('message', 'Failed to update profile'), 400)
            
    except Exception as e:
        app.logger.error(f"Error in update_profile endpoint: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/profile', methods=['GET'])
@require_gemini
def get_profile():
    """
    Get user profile
    
    Query params:
        session_id: Session identifier
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return error_response("session_id query parameter is required")
        
        # Get session
        counselor = get_or_create_session(session_id)
        
        # Get profile
        profile = counselor.get_user_profile()
        
        return success_response({
            "session_id": session_id,
            "profile": profile
        }, "Profile retrieved successfully")
        
    except Exception as e:
        app.logger.error(f"Error in get_profile endpoint: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/history', methods=['GET'])
@require_gemini
def get_history():
    """
    Get conversation history
    
    Query params:
        session_id: Session identifier
        limit: Optional limit on number of messages (default: all)
    """
    try:
        session_id = request.args.get('session_id')
        limit = request.args.get('limit', type=int)
        
        if not session_id:
            return error_response("session_id query parameter is required")
        
        # Get session
        counselor = get_or_create_session(session_id)
        
        # Get history
        history = counselor.get_conversation_history(limit=limit)
        
        return success_response({
            "session_id": session_id,
            "message_count": len(history),
            "history": history
        }, "History retrieved successfully")
        
    except Exception as e:
        app.logger.error(f"Error in get_history endpoint: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/history', methods=['DELETE'])
@require_gemini
def clear_history():
    """
    Clear conversation history
    
    Request JSON:
    {
        "session_id": "session-id"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body must be JSON")
        
        session_id = data.get('session_id')
        
        if not session_id:
            return error_response("session_id is required")
        
        # Get session
        counselor = get_or_create_session(session_id)
        
        # Clear history
        result = counselor.clear_history()
        
        if result['status'] == 'success':
            return success_response({
                "session_id": session_id
            }, "History cleared successfully")
        else:
            return error_response(result.get('message', 'Failed to clear history'), 400)
            
    except Exception as e:
        app.logger.error(f"Error in clear_history endpoint: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/advice/<topic>', methods=['GET'])
@require_gemini
def get_advice(topic: str):
    """
    Get specific career advice on a topic
    
    Path param:
        topic: Career topic (resume, interview, skills, etc.)
    
    Query params:
        session_id: Optional session identifier
    """
    try:
        session_id = request.args.get('session_id', f"advice_{int(datetime.now().timestamp() * 1000)}")
        
        # Get or create session
        counselor = get_or_create_session(session_id)
        
        # Get advice
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
        app.logger.error(f"Error in get_advice endpoint: {traceback.format_exc()}")
        return error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get list of available career advice topics"""
    topics = {
        "resume": "Resume creation and optimization guidance",
        "interview": "Interview preparation and common questions",
        "skills": "In-demand skills and development guidance",
        "career_change": "Career transition strategies",
        "salary": "Salary negotiation techniques",
        "networking": "Professional networking strategies",
        "linkedin": "LinkedIn profile optimization",
        "job_search": "Job search strategies and tips",
        "upskilling": "Skills to learn for career advancement",
        "work_life_balance": "Maintaining healthy work-life balance"
    }
    
    return success_response({
        "topics": topics,
        "usage": "Use GET /api/advice/<topic> to get advice on any topic"
    }, "Topics retrieved successfully")

# -----------------------------
# Error Handlers
# -----------------------------

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return error_response("Endpoint not found", 404)

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors"""
    return error_response("Method not allowed for this endpoint", 405)

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {traceback.format_exc()}")
    return error_response("Internal server error", 500)

# -----------------------------
# Main
# -----------------------------

def main():
    """Run the Flask application"""
    print("🎓 AI Career Counselor API")
    print("=" * 60)
    print()
    
    # Check configuration
    if not GEMINI_SDK_AVAILABLE:
        print("⚠️  WARNING: google-genai SDK not installed")
        print("   Install with: pip install google-genai")
        print()
    
    if not GEMINI_KEY:
        print("⚠️  WARNING: GEMINI_API_KEY not found")
        print("   Set your API key in .env file or environment")
        print("   Get your key from: https://aistudio.google.com/app/apikey")
        print()
    
    if GEMINI_SDK_AVAILABLE and GEMINI_KEY:
        print("✅ Gemini 2.5 Flash configured and ready")
        print()
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting server on http://{host}:{port}")
    print()
    print("API Endpoints:")
    print(f"  • POST   http://{host}:{port}/api/chat")
    print(f"  • POST   http://{host}:{port}/api/profile")
    print(f"  • GET    http://{host}:{port}/api/profile?session_id=<id>")
    print(f"  • GET    http://{host}:{port}/api/history?session_id=<id>")
    print(f"  • DELETE http://{host}:{port}/api/history")
    print(f"  • GET    http://{host}:{port}/api/advice/<topic>")
    print(f"  • GET    http://{host}:{port}/api/topics")
    print(f"  • GET    http://{host}:{port}/api/health")
    print()
    print("📚 Full API documentation at: http://{host}:{port}/")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the app
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()