"""
roadmap_api.py - Career Roadmap Generator Module
Extracted from the original Flask app for modular use
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2
import re

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
