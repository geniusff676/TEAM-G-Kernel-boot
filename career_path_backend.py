# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import PyPDF2
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# import json
# import io

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend

# # Configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'pdf'}
# MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# class CareerPathPlanner:
#     def __init__(self):
#         # Load environment variables from .env file
#         load_dotenv()
        
#         # Configure Gemini API
#         api_key = os.getenv('GEMINI_API_KEY')
#         if not api_key:
#             raise ValueError("GEMINI_API_KEY not found in .env file")
        
#         genai.configure(api_key=api_key)
#         self.model = genai.GenerativeModel('gemini-2.5-flash')
    
#     def extract_text_from_pdf(self, pdf_file):
#         """Extract text content from PDF resume"""
#         try:
#             pdf_reader = PyPDF2.PdfReader(pdf_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#             return text
#         except Exception as e:
#             print(f"Error reading PDF: {e}")
#             return None
    
#     def generate_career_path(self, user_data):
#         """Generate personalized career path using Gemini API with enhanced prompt"""
        
#         # Construct enhanced detailed prompt
#         prompt = f"""
# You are an expert AI career mentor and roadmap planner.

# Your task is to design a **personalized, step-by-step career roadmap** based on the following profile:

# STUDENT/PROFESSIONAL DETAILS:
# - College/University: {user_data.get('college', 'Not provided')}
# - Branch/Major: {user_data.get('branch', 'Not provided')}
# - CGPA/Grade: {user_data.get('cgpa', 'Not provided')}
# - Technical Skills: {user_data.get('skills', 'Not provided')}
# - Interests: {user_data.get('interests', 'Not provided')}
# - Strengths: {user_data.get('strengths', 'Not provided')}
# - Weaknesses: {user_data.get('weaknesses', 'Not provided')}
# - Projects Done: {user_data.get('projects', 'Not provided')}
# - Certifications Done: {user_data.get('certifications_done', 'Not provided')}
# - Internship Experience: {user_data.get('internship_experience', 'Not provided')}
# - Preferred Work Type: {user_data.get('preferred_work_type', 'Not provided')}
# - Desired Job Role: {user_data.get('desired_role', 'Not provided')}
# - Target Industry / Domain: {user_data.get('target_industry', 'Not provided')}
# - Available Hours Per Week: {user_data.get('available_hours_per_week', 'Not provided')}
# - Roadmap Duration: {user_data.get('roadmap_duration', '1 year')}
# - Budget Preference: {user_data.get('budget_preference', 'Not provided')}
# - Learning Style: {user_data.get('learning_style', 'Not provided')}
# - Personality Type: {user_data.get('personality_type', 'Not provided')}
# - Additional Info: {user_data.get('additional_info', 'Not provided')}

# {f"RESUME HIGHLIGHTS: {user_data.get('resume_content', '')[:1000]}" if 'resume_content' in user_data else ''}

# ---

# 🎯 **TASK:**  
# Create a detailed and visually organized **career roadmap** for the user in **{user_data.get('mode', 'detailed')} mode**.
# Follow this format and ensure all outputs are in **structured bullet points with subpoints**.

# ---

# ## 1. POSSIBLE CAREER PATHS
# List 3-4 suitable career tracks based on their skills and interests (e.g., "AI Engineer", "Data Scientist", "Full Stack Developer"),  
# each with:
# • Overview of role
#   → What the role involves
#   → Day-to-day responsibilities
# • Required core skills
#   → Technical skills needed
#   → Soft skills needed
# • Pros & cons
#   → Advantages of this path
#   → Challenges to consider
# • Typical starting positions
#   → Entry-level roles
#   → Junior positions
# • Expected timeline to job-readiness
#   → With their current profile
#   → Estimated months/years

# ---

# ## 2. SELECTED CAREER TRACK: {user_data.get('desired_role', "User's preferred role")}
# Provide a **customized roadmap** based on their current profile and chosen direction.

# ### a. Immediate Action Items (Next 1–3 Months)
# • Quick wins and foundational improvements
#   → Specific daily/weekly actions
#   → Priority skills to start with
# • Resources or short courses to begin with
#   → Course names with platforms and URLs
#   → Free resources available
# • Resume and LinkedIn improvements
#   → Specific sections to enhance
#   → Keywords to add
#   → Profile optimization tips

# ### b. Short-Term Goals (3–6 Months)
# • Skill-building plan
#   → Core technologies to master
#   → Practice platforms (LeetCode, HackerRank, etc.)
#   → Time allocation per skill
# • Real-world projects to build
#   → 2-3 beginner to intermediate projects
#   → Technologies to use
#   → Where to host/showcase
# • Certifications to pursue (free or paid based on budget)
#   → Certification names
#   → Platforms
#   → Expected time commitment
#   → Value in job market
# • Networking & community goals
#   → Communities to join (Reddit, Discord, LinkedIn groups)
#   → Events or webinars to attend
#   → How to contribute

# ### c. Medium-Term Goals (6–12 Months)
# • Advanced skill development
#   → Specialized technologies
#   → Advanced concepts to master
#   → System design and architecture
# • Advanced project ideas
#   → 2-3 intermediate to advanced projects
#   → Real-world problem solving
#   → Technologies and best practices
# • Internship or freelance guidance
#   → Where to find opportunities
#   → How to apply effectively
#   → Portfolio presentation
# • Interview preparation roadmap
#   → DSA preparation strategy
#   → System design practice
#   → Behavioral interview prep
#   → Mock interview platforms

# ### d. Long-Term Career Path (1–3 Years)
# • Specialization focus
#   → Areas to deep-dive
#   → Industry certifications
#   → Emerging technologies to watch
# • Transition opportunities
#   → Career progression paths
#   → Salary expectations at each level
#   → Geographic opportunities
# • Leadership and growth roadmap
#   → Soft skills development
#   → Mentorship opportunities
#   → Contributing to open source
#   → Building personal brand

# ---

# ## 3. SKILLS GAP ANALYSIS
# • Current Skills Assessment
#   → Skills they already have
#   → Proficiency levels
# • Required Industry Skills
#   → Must-have skills for desired role
#   → Nice-to-have skills
#   → Emerging skills in the industry
# • Priority Learning Order
#   → Skill 1 (Why first, estimated time)
#   → Skill 2 (Why next, estimated time)
#   → Skill 3 (Why after, estimated time)
# • Estimated Timeline
#   → Time to become job-ready
#   → Milestones to track progress

# ---

# ## 4. PROJECT IDEAS (Practical Portfolio Builders)
# For each project (3–5 projects):
# • Project Name
#   → Brief description
#   → Problem it solves
# • Tech Stack
#   → Frontend technologies
#   → Backend technologies
#   → Database and tools
# • Learning Outcomes
#   → Skills demonstrated
#   → Complexity level
# • Implementation Tips
#   → Where to start
#   → Resources to use
#   → Time estimate
# • Showcase Strategy
#   → GitHub repository structure
#   → Live demo hosting
#   → README documentation

# ---

# ## 5. COURSES & RESOURCES
# For each key skill area, recommend:
# • Course Title
#   → Full name of course
# • Platform & URL
#   → Coursera, Udemy, edX, freeCodeCamp, etc.
#   → Direct link if possible
# • Duration & Effort
#   → Hours per week
#   → Total weeks/months
# • Why It's Relevant
#   → How it aligns with career goals
#   → Skills covered
# • Cost Indicator
#   → Free / Paid / Free with certificate option
#   → Fits their budget preference: {user_data.get('budget_preference', 'Affordable')}
# • Learning Path Integration
#   → When to take this course
#   → Prerequisites if any

# Include resources matching their learning style: {user_data.get('learning_style', 'Mixed')}

# ---

# ## 6. NETWORKING & PERSONAL BRANDING
# • Online Communities to Join
#   → Platform-specific communities
#   → Why each community is valuable
#   → How to actively participate
# • LinkedIn Strategy
#   → Profile optimization checklist
#   → Content posting strategy
#   → Connection building approach
#   → Engagement tips
# • GitHub Strategy
#   → Repository organization
#   → Contributing to open source
#   → Building visibility
#   → README best practices
# • Conferences, Hackathons & Events
#   → Relevant events to attend
#   → How to prepare
#   → Networking strategies
# • Personal Brand Building
#   → Blog or portfolio website
#   → Social media presence
#   → Building thought leadership

# ---

# ## 7. JOB SEARCH STRATEGY
# • Resume Optimization
#   → ATS-friendly formatting
#   → Key sections to highlight
#   → Action verbs to use
#   → Quantifying achievements
# • Company Targeting Strategy
#   → Startups vs Product companies vs MNCs
#   → Based on preference: {user_data.get('preferred_work_type', 'Flexible')}
#   → Research approach
# • Job Search Platforms
#   → LinkedIn, Indeed, AngelList, etc.
#   → Company career pages
#   → Referral strategies
# • Application Strategy
#   → Number of applications per week
#   → Customization approach
#   → Follow-up tactics
# • Interview Preparation
#   → Technical interview prep timeline
#   → Behavioral questions practice
#   → Mock interview platforms
#   → Salary negotiation tips

# ---

# ## 8. ADDITIONAL RECOMMENDATIONS
# • Books to Read
#   → Technical books
#   → Career development books
#   → Industry-specific reads
# • YouTube Channels to Follow
#   → Channel names with focus areas
#   → Why each channel is valuable
# • Podcasts for Learning & Inspiration
#   → Podcast names
#   → Key topics covered
# • Thought Leaders & Mentors
#   → Industry experts to follow
#   → Where to find them (Twitter, LinkedIn, etc.)
# • Learning Resources
#   → Documentation sites
#   → Tutorial platforms
#   → Practice platforms

# ---

# ## 9. TIMELINE & MILESTONES
# Create a visual timeline for {user_data.get('roadmap_duration', '1 year')} with:
# • Month-by-month breakdown
#   → What to focus on each month
#   → Key milestones
#   → Deliverables
# • Progress Tracking Metrics
#   → How to measure progress
#   → KPIs for success
# • Adjustment Points
#   → When to reassess
#   → How to pivot if needed

# ---

# ## 10. MOTIVATION & MINDSET
# • Realistic Expectations
#   → What to expect in this journey
#   → Common challenges
# • Staying Motivated
#   → Tips for consistency
#   → Handling setbacks
# • Work-Life Balance
#   → Given {user_data.get('available_hours_per_week', '10-15')} hours/week
#   → Avoiding burnout
# • Success Stories
#   → Similar profiles who succeeded
#   → Inspiration and proof of concept

# ---

# **Output Format Rules:**
# - Use clear bullet points (•) with nested subpoints (→ or —)
# - Keep tone motivational yet realistic
# - Organize each section with headers (##) and subheaders (###)
# - Align recommendations with:
#   * Available time: {user_data.get('available_hours_per_week', '10-15')} hours/week
#   * Roadmap duration: {user_data.get('roadmap_duration', '1 year')}
#   * Budget: {user_data.get('budget_preference', 'Affordable')}
#   * Learning style: {user_data.get('learning_style', 'Mixed')}
#   * Personality: {user_data.get('personality_type', 'Balanced')}
# - Provide specific, actionable advice with URLs where possible
# - Format in {user_data.get('mode', 'detailed')} mode

# Generate the roadmap now.
# """
        
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             raise Exception(f"Error generating career path: {e}")


# # Helper functions
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # Initialize planner
# planner = CareerPathPlanner()


# # API Routes
# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'success',
#         'message': 'Career Path Planner API is running'
#     }), 200


# @app.route('/api/upload-resume', methods=['POST'])
# def upload_resume():
#     """
#     Upload and process resume PDF
#     Returns extracted text from the resume
#     """
#     try:
#         # Check if file is present
#         if 'resume' not in request.files:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No resume file provided'
#             }), 400
        
#         file = request.files['resume']
        
#         # Check if file is selected
#         if file.filename == '':
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No file selected'
#             }), 400
        
#         # Check if file is allowed
#         if not allowed_file(file.filename):
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Only PDF files are allowed'
#             }), 400
        
#         # Extract text from PDF
#         resume_text = planner.extract_text_from_pdf(file)
        
#         if not resume_text:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Could not extract text from PDF'
#             }), 400
        
#         return jsonify({
#             'status': 'success',
#             'message': 'Resume processed successfully',
#             'data': {
#                 'resume_content': resume_text,
#                 'filename': secure_filename(file.filename)
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': f'Error processing resume: {str(e)}'
#         }), 500


# @app.route('/api/generate-roadmap', methods=['POST'])
# def generate_roadmap():
#     """
#     Generate career roadmap based on user data
#     Expects JSON data with user information
#     """
#     try:
#         # Get JSON data from request
#         user_data = request.get_json()
        
#         if not user_data:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No data provided'
#             }), 400
        
#         # Validate required fields
#         required_fields = ['desired_role']
#         missing_fields = [field for field in required_fields if field not in user_data or not user_data[field]]
        
#         if missing_fields:
#             return jsonify({
#                 'status': 'error',
#                 'message': f'Missing required fields: {", ".join(missing_fields)}'
#             }), 400
        
#         # Generate career roadmap
#         roadmap = planner.generate_career_path(user_data)
        
#         # Save roadmap to file (optional)
#         filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_').replace('/', '_')}.txt"
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write("="*80 + "\n")
#             f.write("PERSONALIZED CAREER ROADMAP\n")
#             f.write("="*80 + "\n\n")
#             f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
#             f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
#             f.write(f"Branch: {user_data.get('branch', 'N/A')}\n")
#             f.write(f"Duration: {user_data.get('roadmap_duration', 'N/A')}\n")
#             f.write(f"Mode: {user_data.get('mode', 'detailed').title()}\n")
#             f.write("\n" + "="*80 + "\n\n")
#             f.write(roadmap)
        
#         return jsonify({
#             'status': 'success',
#             'message': 'Career roadmap generated successfully',
#             'data': {
#                 'roadmap': roadmap,
#                 'saved_file': filename,
#                 'user_profile': {
#                     'college': user_data.get('college', 'N/A'),
#                     'desired_role': user_data.get('desired_role', 'N/A'),
#                     'branch': user_data.get('branch', 'N/A'),
#                     'duration': user_data.get('roadmap_duration', 'N/A')
#                 }
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': f'Error generating roadmap: {str(e)}'
#         }), 500


# @app.route('/api/generate-roadmap-with-resume', methods=['POST'])
# def generate_roadmap_with_resume():
#     """
#     Complete flow: Upload resume and generate roadmap in one request
#     Expects multipart/form-data with:
#     - resume: PDF file
#     - data: JSON string with user information
#     """
#     try:
#         # Check if resume file is present
#         if 'resume' not in request.files:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No resume file provided'
#             }), 400
        
#         file = request.files['resume']
        
#         # Check if file is selected
#         if file.filename == '':
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No file selected'
#             }), 400
        
#         # Check if file is allowed
#         if not allowed_file(file.filename):
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Only PDF files are allowed'
#             }), 400
        
#         # Extract resume text
#         resume_text = planner.extract_text_from_pdf(file)
        
#         if not resume_text:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'Could not extract text from PDF'
#             }), 400
        
#         # Get user data from form
#         user_data_str = request.form.get('data')
#         if not user_data_str:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No user data provided'
#             }), 400
        
#         user_data = json.loads(user_data_str)
        
#         # Add resume content to user data
#         user_data['resume_content'] = resume_text
        
#         # Validate required fields
#         required_fields = ['desired_role']
#         missing_fields = [field for field in required_fields if field not in user_data or not user_data[field]]
        
#         if missing_fields:
#             return jsonify({
#                 'status': 'error',
#                 'message': f'Missing required fields: {", ".join(missing_fields)}'
#             }), 400
        
#         # Generate career roadmap
#         roadmap = planner.generate_career_path(user_data)
        
#         # Save roadmap to file
#         filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_').replace('/', '_')}.txt"
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write("="*80 + "\n")
#             f.write("PERSONALIZED CAREER ROADMAP\n")
#             f.write("="*80 + "\n\n")
#             f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
#             f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
#             f.write(f"Branch: {user_data.get('branch', 'N/A')}\n")
#             f.write(f"Duration: {user_data.get('roadmap_duration', 'N/A')}\n")
#             f.write(f"Mode: {user_data.get('mode', 'detailed').title()}\n")
#             f.write("\n" + "="*80 + "\n\n")
#             f.write(roadmap)
        
#         return jsonify({
#             'status': 'success',
#             'message': 'Resume processed and career roadmap generated successfully',
#             'data': {
#                 'roadmap': roadmap,
#                 'saved_file': filename,
#                 'resume_processed': True,
#                 'user_profile': {
#                     'college': user_data.get('college', 'N/A'),
#                     'desired_role': user_data.get('desired_role', 'N/A'),
#                     'branch': user_data.get('branch', 'N/A'),
#                     'duration': user_data.get('roadmap_duration', 'N/A')
#                 }
#             }
#         }), 200
        
#     except json.JSONDecodeError:
#         return jsonify({
#             'status': 'error',
#             'message': 'Invalid JSON data format'
#         }), 400
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': f'Error processing request: {str(e)}'
#         }), 500


# @app.errorhandler(413)
# def request_entity_too_large(error):
#     return jsonify({
#         'status': 'error',
#         'message': 'File too large. Maximum size is 16MB'
#     }), 413


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         'status': 'error',
#         'message': 'Endpoint not found'
#     }), 404


# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({
#         'status': 'error',
#         'message': 'Internal server error'
#     }), 500


# if __name__ == "__main__":
#     print("\n" + "="*80)
#     print("CAREER PATH PLANNER API SERVER".center(80))
#     print("="*80 + "\n")
#     print("🚀 Starting Flask server...")
#     print("📡 API Endpoints:")
#     print("   - GET  /api/health")
#     print("   - POST /api/upload-resume")
#     print("   - POST /api/generate-roadmap")
#     print("   - POST /api/generate-roadmap-with-resume")
#     print("\n" + "="*80 + "\n")
    
#     app.run(debug=True, host='0.0.0.0', port=5002)



import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import io
import re
import sqlite3


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


class CareerPathPlanner:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text content from PDF resume"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def generate_career_path(self, user_data):
        """Generate concise, structured career roadmap"""
        
        duration = user_data.get('roadmap_duration', '6 months')
        
        # Simplified, focused prompt
        prompt = f"""
You are an AI career mentor. Create a CONCISE, actionable {duration} career roadmap.

PROFILE:
- Role Goal: {user_data.get('desired_role', 'Not provided')}
- Branch: {user_data.get('branch', 'Not provided')}
- Skills: {user_data.get('skills', 'Not provided')}
- CGPA: {user_data.get('cgpa', 'Not provided')}
- Experience: {user_data.get('internship_experience', 'None')}
- Weekly Hours: {user_data.get('available_hours_per_week', '10-15')}
- Budget: {user_data.get('budget_preference', 'Affordable')}

{f"RESUME: {user_data.get('resume_content', '')[:800]}" if 'resume_content' in user_data else ''}

---

OUTPUT FORMAT (STRICT):

## 1. RECOMMENDED PATH
• Primary role: [Role name]
  → Why it fits: [1-2 sentences]
  → Timeline to job-ready: [X months]
  → Key skills needed: [3-5 skills]

## 2. SKILLS GAP
• Must learn: [Skill 1], [Skill 2], [Skill 3]
• Already have: [Current skills assessment]
• Learning priority: [Ordered list with time estimates]

## 3. MONTHLY ROADMAP

### Month 1: [Focus Area]
• Goals:
  → [Goal 1]
  → [Goal 2]
• Tasks:
  → [Task 1 with time estimate]
  → [Task 2 with time estimate]
• Resources:
  → [Resource 1 - Platform - URL if free]
  → [Resource 2 - Platform - URL if free]
• Deliverable: [What to build/achieve]

### Month 2: [Focus Area]
• Goals:
  → [Goal 1]
  → [Goal 2]
• Tasks:
  → [Task 1 with time estimate]
  → [Task 2 with time estimate]
• Resources:
  → [Resource 1 - Platform - URL if free]
  → [Resource 2 - Platform - URL if free]
• Deliverable: [What to build/achieve]

[Continue for {duration}]

## 4. PROJECT IDEAS (3 Projects)
### Project 1: [Name]
• Tech stack: [Technologies]
• Purpose: [1 sentence]
• Duration: [X weeks]
• Showcase: [GitHub + live demo]

[Project 2 and 3 similar format]

## 5. TOP RESOURCES
• Course 1: [Name] - [Platform] - [URL] - [Duration] - [Free/Paid]
• Course 2: [Name] - [Platform] - [URL] - [Duration] - [Free/Paid]
• Course 3: [Name] - [Platform] - [URL] - [Duration] - [Free/Paid]
• Practice: [Platform names]

## 6. JOB PREP CHECKLIST
• Resume: [2-3 key improvements]
• LinkedIn: [2-3 optimization tips]
• Portfolio: [What to include]
• Interview prep: [Focus areas]
• Application strategy: [Where and how]

## 7. QUICK WINS (Start Today)
• Week 1: [Immediate action]
• Week 2: [Immediate action]
• Week 3: [Immediate action]

---

RULES:
- Keep total output under 2000 words
- Use bullet points (•) and arrows (→) only
- Be specific with course names and URLs
- Include only {duration} months in roadmap
- Focus on practical, actionable items
- Match budget: {user_data.get('budget_preference', 'Affordable')}
- No fluff or motivational content
- Each month should have max 2-3 goals, 3-4 tasks, 2-3 resources

Generate now.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating career path: {e}")
    
    def parse_roadmap_to_json(self, roadmap_text):
        """Parse markdown roadmap into structured JSON"""
        
        structured_data = {
            "recommended_path": {},
            "skills_gap": {},
            "monthly_roadmap": [],
            "projects": [],
            "resources": [],
            "job_prep": {},
            "quick_wins": []
        }
        
        try:
            lines = roadmap_text.split('\n')
            current_section = None
            current_month = None
            current_project = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                if '## 1. RECOMMENDED PATH' in line:
                    current_section = 'recommended_path'
                elif '## 2. SKILLS GAP' in line:
                    current_section = 'skills_gap'
                elif '## 3. MONTHLY ROADMAP' in line:
                    current_section = 'monthly_roadmap'
                elif '## 4. PROJECT IDEAS' in line:
                    current_section = 'projects'
                elif '## 5. TOP RESOURCES' in line:
                    current_section = 'resources'
                elif '## 6. JOB PREP CHECKLIST' in line:
                    current_section = 'job_prep'
                elif '## 7. QUICK WINS' in line:
                    current_section = 'quick_wins'
                
                # Parse month headers
                elif line.startswith('### Month') and current_section == 'monthly_roadmap':
                    if current_month:
                        structured_data['monthly_roadmap'].append(current_month)
                    
                    month_match = re.match(r'### Month (\d+):\s*(.+)', line)
                    if month_match:
                        current_month = {
                            "month": int(month_match.group(1)),
                            "focus": month_match.group(2),
                            "goals": [],
                            "tasks": [],
                            "resources": [],
                            "deliverable": ""
                        }
                
                # Parse month content
                elif current_month and current_section == 'monthly_roadmap':
                    if '• Goals:' in line:
                        subsection = 'goals'
                    elif '• Tasks:' in line:
                        subsection = 'tasks'
                    elif '• Resources:' in line:
                        subsection = 'resources'
                    elif '• Deliverable:' in line:
                        subsection = 'deliverable'
                    elif line.startswith('→'):
                        content = line.replace('→', '').strip()
                        if subsection == 'goals':
                            current_month['goals'].append(content)
                        elif subsection == 'tasks':
                            current_month['tasks'].append(content)
                        elif subsection == 'resources':
                            current_month['resources'].append(content)
                    elif subsection == 'deliverable' and line.startswith('•'):
                        current_month['deliverable'] = line.replace('•', '').replace('Deliverable:', '').strip()
                
                # Parse projects
                elif line.startswith('### Project') and current_section == 'projects':
                    if current_project:
                        structured_data['projects'].append(current_project)
                    
                    project_match = re.match(r'### Project \d+:\s*(.+)', line)
                    if project_match:
                        current_project = {
                            "name": project_match.group(1),
                            "tech_stack": "",
                            "purpose": "",
                            "duration": "",
                            "showcase": ""
                        }
                
                elif current_project and current_section == 'projects':
                    if line.startswith('• Tech stack:'):
                        current_project['tech_stack'] = line.replace('• Tech stack:', '').strip()
                    elif line.startswith('• Purpose:'):
                        current_project['purpose'] = line.replace('• Purpose:', '').strip()
                    elif line.startswith('• Duration:'):
                        current_project['duration'] = line.replace('• Duration:', '').strip()
                    elif line.startswith('• Showcase:'):
                        current_project['showcase'] = line.replace('• Showcase:', '').strip()
                
                # Parse resources
                elif current_section == 'resources' and line.startswith('•'):
                    resource_text = line.replace('•', '').strip()
                    if resource_text and 'Course' not in resource_text and 'Practice' not in resource_text:
                        structured_data['resources'].append(resource_text)
            
            # Add last month and project
            if current_month:
                structured_data['monthly_roadmap'].append(current_month)
            if current_project:
                structured_data['projects'].append(current_project)
            
            return structured_data
            
        except Exception as e:
            print(f"Error parsing roadmap: {e}")
            return {"raw_text": roadmap_text, "parsing_error": str(e)}


# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Initialize planner
planner = CareerPathPlanner()


# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'Career Path Planner API is running'
    }), 200


@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No resume file provided'
            }), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Only PDF files are allowed'
            }), 400
        
        resume_text = planner.extract_text_from_pdf(file)
        
        if not resume_text:
            return jsonify({
                'status': 'error',
                'message': 'Could not extract text from PDF'
            }), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Resume processed successfully',
            'data': {
                'resume_content': resume_text,
                'filename': secure_filename(file.filename)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing resume: {str(e)}'
        }), 500


@app.route('/api/generate-roadmap', methods=['POST'])
def generate_roadmap():
    try:
        user_data = request.get_json()
        
        if not user_data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        required_fields = ['desired_role']
        missing_fields = [field for field in required_fields if field not in user_data or not user_data[field]]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Generate concise roadmap
        roadmap_text = planner.generate_career_path(user_data)
        
        # Parse into structured JSON
        roadmap_structured = planner.parse_roadmap_to_json(roadmap_text)
        
        # Save roadmap
        filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_').replace('/', '_')}.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("PERSONALIZED CAREER ROADMAP\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
            f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
            f.write(f"Duration: {user_data.get('roadmap_duration', '6 months')}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(roadmap_text)
        
        return jsonify({
            'status': 'success',
            'message': 'Career roadmap generated successfully',
            'data': {
                'roadmap_text': roadmap_text,
                'roadmap_structured': roadmap_structured,
                'saved_file': filename,
                'user_profile': {
                    'college': user_data.get('college', 'N/A'),
                    'desired_role': user_data.get('desired_role', 'N/A'),
                    'branch': user_data.get('branch', 'N/A'),
                    'duration': user_data.get('roadmap_duration', '6 months')
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error generating roadmap: {str(e)}'
        }), 500

# @app.route('/api/generate-roadmap', methods=['POST'])
# def generate_roadmap():
#     try:
#         import sqlite3, json

#         user_data = request.get_json()
#         if not user_data:
#             return jsonify({'status': 'error', 'message': 'No data provided'}), 400

#         # ✅ Require user_id and desired_role
#         required_fields = ['user_id', 'desired_role']
#         missing_fields = [f for f in required_fields if f not in user_data or not user_data[f]]
#         if missing_fields:
#             return jsonify({
#                 'status': 'error',
#                 'message': f'Missing required fields: {", ".join(missing_fields)}'
#             }), 400

#         user_id = user_data['user_id']

#         # --------------------------------------
#         # 🧩 Check if career_path exists in DB
#         # --------------------------------------
#         conn = sqlite3.connect('user_data.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT career_path FROM users WHERE user_id = ?", (user_id,))
#         row = cursor.fetchone()

#         if row and row[0]:  # Already has a roadmap
#             print(f"✅ Existing roadmap found for user_id {user_id}")
#             roadmap_json = json.loads(row[0])
#             conn.close()
#             return jsonify({
#                 'status': 'success',
#                 'message': 'Existing career roadmap retrieved successfully',
#                 'data': {
#                     'roadmap_structured': roadmap_json,
#                     'user_profile': {
#                         'college': user_data.get('college', 'N/A'),
#                         'desired_role': user_data.get('desired_role', 'N/A'),
#                         'branch': user_data.get('branch', 'N/A')
#                     }
#                 }
#             }), 200
#         conn.close()

#         # 🧠 Generate new roadmap if none exists
#         roadmap_text = planner.generate_career_path(user_data)
#         roadmap_structured = planner.parse_roadmap_to_json(roadmap_text)

#         # 🗃️ Store the new roadmap JSON in DB
#         conn = sqlite3.connect('user_data.db')
#         cursor = conn.cursor()
#         roadmap_json_str = json.dumps(roadmap_structured)

#         cursor.execute("""
#             UPDATE users SET career_path = ?
#             WHERE user_id = ?
#         """, (roadmap_json_str, user_id))
#         conn.commit()
#         conn.close()

#         # Save to file (optional)
#         filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_')}.txt"
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write("="*80 + "\n")
#             f.write("PERSONALIZED CAREER ROADMAP\n")
#             f.write("="*80 + "\n\n")
#             f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
#             f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
#             f.write(f"Duration: {user_data.get('roadmap_duration', '6 months')}\n")
#             f.write("\n" + "="*80 + "\n\n")
#             f.write(roadmap_text)
#         print(roadmap_json)
#         return jsonify({
#             'status': 'success',
#             'message': 'New career roadmap generated and saved successfully',
#             'data': {
#                 'roadmap_text': roadmap_text,
#                 'roadmap_structured': roadmap_structured,
#                 'saved_file': filename,
#                 'user_profile': {
#                     'college': user_data.get('college', 'N/A'),
#                     'desired_role': user_data.get('desired_role', 'N/A'),
#                     'branch': user_data.get('branch', 'N/A'),
#                     'duration': user_data.get('roadmap_duration', '6 months')
#                 }
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({'status': 'error', 'message': f'Error generating roadmap: {str(e)}'}), 500


@app.route('/api/generate-roadmap-with-resume', methods=['POST'])
def generate_roadmap_with_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No resume file provided'
            }), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Only PDF files are allowed'
            }), 400
        
        resume_text = planner.extract_text_from_pdf(file)
        
        if not resume_text:
            return jsonify({
                'status': 'error',
                'message': 'Could not extract text from PDF'
            }), 400
        
        user_data_str = request.form.get('data')
        if not user_data_str:
            return jsonify({
                'status': 'error',
                'message': 'No user data provided'
            }), 400
        
        user_data = json.loads(user_data_str)
        user_data['resume_content'] = resume_text
        
        required_fields = ['desired_role']
        missing_fields = [field for field in required_fields if field not in user_data or not user_data[field]]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Generate roadmap
        roadmap_text = planner.generate_career_path(user_data)
        roadmap_structured = planner.parse_roadmap_to_json(roadmap_text)
        
        # Save roadmap
        filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_').replace('/', '_')}.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("PERSONALIZED CAREER ROADMAP\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
            f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
            f.write(f"Duration: {user_data.get('roadmap_duration', '6 months')}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(roadmap_text)
        
        return jsonify({
            'status': 'success',
            'message': 'Resume processed and career roadmap generated successfully',
            'data': {
                'roadmap_text': roadmap_text,
                'roadmap_structured': roadmap_structured,
                'saved_file': filename,
                'resume_processed': True,
                'user_profile': {
                    'college': user_data.get('college', 'N/A'),
                    'desired_role': user_data.get('desired_role', 'N/A'),
                    'branch': user_data.get('branch', 'N/A'),
                    'duration': user_data.get('roadmap_duration', '6 months')
                }
            }
        }), 200
        
    except json.JSONDecodeError:
        return jsonify({
            'status': 'error',
            'message': 'Invalid JSON data format'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing request: {str(e)}'
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'status': 'error',
        'message': 'File too large. Maximum size is 16MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == "__main__":
    print("\n" + "="*80)
    print("CAREER PATH PLANNER API SERVER".center(80))
    print("="*80 + "\n")
    print("🚀 Starting Flask server...")
    print("📡 API Endpoints:")
    print("   - GET  /api/health")
    print("   - POST /api/upload-resume")
    print("   - POST /api/generate-roadmap")
    print("   - POST /api/generate-roadmap-with-resume")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5002)