# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import os
# import re
# import requests
# from typing import Dict, List, Optional
# import tempfile
# import shutil
# from pathlib import Path

# # Import functions from existing files
# import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # LangChain/LangGraph imports for OpenAI
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.prompts import ChatPromptTemplate
# from langgraph.graph import StateGraph, END
# from typing_extensions import TypedDict

# app = Flask(__name__)
# CORS(app)

# # Configuration
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Set your API key
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')  # Optional: for higher rate limits

# # Initialize LLM with OpenAI
# llm = ChatOpenAI(
#     model="gpt-4o",  # You can also use "gpt-4-turbo", "gpt-4", or "gpt-3.5-turbo"
#     api_key=OPENAI_API_KEY,
#     temperature=0.7
# )

# # ============================================================================
# # State Definition for LangGraph
# # ============================================================================

# class ResumeState(TypedDict):
#     original_latex: str
#     job_description: str
#     github_username: Optional[str]
#     github_repos: List[Dict]
#     publications: Optional[str]
#     awards: Optional[str]
#     honors: Optional[str]
#     parsed_sections: Dict
#     updated_content: Dict
#     final_latex: str
#     error: Optional[str]

# # ============================================================================
# # GitHub Integration Functions
# # ============================================================================

# def fetch_github_repositories(username: str, token: Optional[str] = None) -> List[Dict]:
#     """
#     Fetch user's GitHub repositories
#     """
#     try:
#         headers = {}
#         if token:
#             headers['Authorization'] = f'token {token}'
        
#         url = f'https://api.github.com/users/{username}/repos'
#         response = requests.get(
#             url,
#             headers=headers,
#             params={'per_page': 100, 'sort': 'updated', 'type': 'owner'}
#         )
#         response.raise_for_status()
        
#         repos = response.json()
        
#         # Get detailed info for each repo
#         repo_details = []
#         for repo in repos[:20]:  # Limit to top 20 most recent
#             repo_info = {
#                 'name': repo['name'],
#                 'description': repo.get('description', ''),
#                 'language': repo.get('language', ''),
#                 'stars': repo.get('stargazers_count', 0),
#                 'forks': repo.get('forks_count', 0),
#                 'url': repo['html_url'],
#                 'topics': repo.get('topics', []),
#                 'created_at': repo.get('created_at', ''),
#                 'updated_at': repo.get('updated_at', ''),
#             }
            
#             # Try to get README
#             try:
#                 readme_url = f"https://api.github.com/repos/{username}/{repo['name']}/readme"
#                 readme_resp = requests.get(readme_url, headers=headers)
#                 if readme_resp.status_code == 200:
#                     readme_data = readme_resp.json()
#                     # Get raw content
#                     content_resp = requests.get(readme_data['download_url'])
#                     if content_resp.status_code == 200:
#                         repo_info['readme'] = content_resp.text[:1000]  # First 1000 chars
#             except:
#                 pass
            
#             repo_details.append(repo_info)
        
#         return repo_details
    
#     except Exception as e:
#         print(f"Error fetching GitHub repos: {str(e)}")
#         return []

# # ============================================================================
# # LaTeX Parsing Functions
# # ============================================================================

# def parse_latex_resume(latex_content: str) -> Dict:
#     """
#     Parse LaTeX resume to extract sections
#     """
#     sections = {
#         'projects': '',
#         'publications': '',
#         'awards': '',
#         'honors': '',
#         'experience': '',
#         'education': '',
#         'skills': '',
#         'raw_content': latex_content
#     }
    
#     # Find sections using common LaTeX section markers
#     section_patterns = {
#         'projects': r'\\section\*?{[Pp]rojects?}(.*?)(?=\\section|\Z)',
#         'publications': r'\\section\*?{[Pp]ublications?}(.*?)(?=\\section|\Z)',
#         'awards': r'\\section\*?{[Aa]wards?}(.*?)(?=\\section|\Z)',
#         'honors': r'\\section\*?{[Hh]onors?}(.*?)(?=\\section|\Z)',
#         'experience': r'\\section\*?{[Ee]xperience}(.*?)(?=\\section|\Z)',
#         'education': r'\\section\*?{[Ee]ducation}(.*?)(?=\\section|\Z)',
#         'skills': r'\\section\*?{[Ss]kills?}(.*?)(?=\\section|\Z)',
#     }
    
#     for section_name, pattern in section_patterns.items():
#         match = re.search(pattern, latex_content, re.DOTALL | re.IGNORECASE)
#         if match:
#             sections[section_name] = match.group(0)
    
#     return sections

# def replace_section_in_latex(original_latex: str, section_name: str, new_content: str) -> str:
#     """
#     Replace a specific section in LaTeX while preserving template structure
#     """
#     # Find the section
#     pattern = rf'(\\section\*?{{{section_name}}})(.*?)(?=\\section|\Z)'
    
#     # Check if section exists
#     match = re.search(pattern, original_latex, re.DOTALL | re.IGNORECASE)
    
#     if match:
#         # Replace the content after the section header
#         section_header = match.group(1)
#         replacement = f"{section_header}\n{new_content}\n"
#         updated_latex = re.sub(pattern, replacement, original_latex, count=1, flags=re.DOTALL | re.IGNORECASE)
#         return updated_latex
#     else:
#         # Section doesn't exist, append it before \end{document}
#         end_doc_pattern = r'(\\end{document})'
#         new_section = f"\n\\section{{{section_name}}}\n{new_content}\n\n"
#         updated_latex = re.sub(end_doc_pattern, new_section + r'\1', original_latex)
#         return updated_latex

# # ============================================================================
# # LangGraph Node Functions
# # ============================================================================

# def parse_resume_node(state: ResumeState) -> ResumeState:
#     """Parse the original LaTeX resume into sections"""
#     try:
#         sections = parse_latex_resume(state['original_latex'])
#         state['parsed_sections'] = sections
#         return state
#     except Exception as e:
#         state['error'] = f"Error parsing resume: {str(e)}"
#         return state

# def fetch_github_node(state: ResumeState) -> ResumeState:
#     """Fetch GitHub repositories if username provided"""
#     if state.get('github_username'):
#         try:
#             repos = fetch_github_repositories(state['github_username'], GITHUB_TOKEN)
#             state['github_repos'] = repos
#         except Exception as e:
#             print(f"Warning: Could not fetch GitHub repos: {str(e)}")
#             state['github_repos'] = []
#     else:
#         state['github_repos'] = []
    
#     return state

# def analyze_and_update_projects_node(state: ResumeState) -> ResumeState:
#     """Use LLM to select and format relevant projects based on job description"""
#     try:
#         job_desc = state['job_description']
#         repos = state['github_repos']
#         current_projects = state['parsed_sections'].get('projects', '')
        
#         # Create prompt for LLM
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", """You are an expert resume writer specializing in LaTeX formatting. 
# Your task is to select and format the most relevant projects for a job application based on:
# 1. The job description
# 2. GitHub repositories
# 3. Current projects in the resume

# Follow these guidelines:
# - Select 3-5 most relevant projects that match the job requirements
# - Maintain the EXACT LaTeX formatting style from the original resume
# - Highlight technical skills and technologies mentioned in the job description
# - Include quantifiable achievements where possible
# - Keep the same LaTeX environment structure (itemize, description, etc.)
# - DO NOT change LaTeX commands or document structure
# - Output ONLY the LaTeX code for the projects section content (not including \\section header)"""),
#             ("human", """
# Job Description:
# {job_desc}

# GitHub Repositories:
# {repos}

# Current Projects Section:
# {current_projects}

# Generate an updated projects section in LaTeX format that highlights the most relevant projects for this job.
# Maintain the exact same LaTeX formatting style as the current projects section.
# Output ONLY the content (no section header).
# """)
#         ])
        
#         messages = prompt.format_messages(
#             job_desc=job_desc,
#             repos=str(repos),
#             current_projects=current_projects
#         )
#         response = llm.invoke(messages)
#         updated_projects = response.content
        
#         if 'updated_content' not in state:
#             state['updated_content'] = {}
#         state['updated_content']['projects'] = updated_projects
        
#     except Exception as e:
#         state['error'] = f"Error updating projects: {str(e)}"
    
#     return state

# def update_publications_awards_node(state: ResumeState) -> ResumeState:
#     """Update publications, awards, and honors sections"""
#     try:
#         if 'updated_content' not in state:
#             state['updated_content'] = {}
        
#         # Get current sections
#         current_publications = state['parsed_sections'].get('publications', '')
#         current_awards = state['parsed_sections'].get('awards', '')
#         current_honors = state['parsed_sections'].get('honors', '')
        
#         # Update publications if provided
#         if state.get('publications'):
#             prompt = ChatPromptTemplate.from_messages([
#                 ("system", """You are an expert at formatting publications in LaTeX for resumes.
# Maintain the EXACT LaTeX formatting style from the original resume.
# Output ONLY the LaTeX code for the content (not including \\section header)."""),
#                 ("human", """
# Current Publications Section:
# {current_publications}

# New Publications to Add:
# {new_publications}

# Job Description (for relevance):
# {job_desc}

# Generate an updated publications section in LaTeX format, prioritizing those most relevant to the job.
# Maintain the exact same LaTeX formatting style.
# Output ONLY the content.
# """)
#             ])
            
#             messages = prompt.format_messages(
#                 current_publications=current_publications,
#                 new_publications=state['publications'],
#                 job_desc=state['job_description']
#             )
#             response = llm.invoke(messages)
#             state['updated_content']['publications'] = response.content
        
#         # Update awards if provided
#         if state.get('awards'):
#             prompt = ChatPromptTemplate.from_messages([
#                 ("system", """You are an expert at formatting awards in LaTeX for resumes.
# Maintain the EXACT LaTeX formatting style from the original resume.
# Output ONLY the LaTeX code for the content (not including \\section header)."""),
#                 ("human", """
# Current Awards Section:
# {current_awards}

# New Awards to Add:
# {new_awards}

# Job Description (for relevance):
# {job_desc}

# Generate an updated awards section in LaTeX format, prioritizing those most relevant to the job.
# Maintain the exact same LaTeX formatting style.
# Output ONLY the content.
# """)
#             ])
            
#             messages = prompt.format_messages(
#                 current_awards=current_awards,
#                 new_awards=state['awards'],
#                 job_desc=state['job_description']
#             )
#             response = llm.invoke(messages)
#             state['updated_content']['awards'] = response.content
        
#         # Update honors if provided
#         if state.get('honors'):
#             prompt = ChatPromptTemplate.from_messages([
#                 ("system", """You are an expert at formatting honors in LaTeX for resumes.
# Maintain the EXACT LaTeX formatting style from the original resume.
# Output ONLY the LaTeX code for the content (not including \\section header)."""),
#                 ("human", """
# Current Honors Section:
# {current_honors}

# New Honors to Add:
# {new_honors}

# Job Description (for relevance):
# {job_desc}

# Generate an updated honors section in LaTeX format, prioritizing those most relevant to the job.
# Maintain the exact same LaTeX formatting style.
# Output ONLY the content.
# """)
#             ])
            
#             messages = prompt.format_messages(
#                 current_honors=current_honors,
#                 new_honors=state['honors'],
#                 job_desc=state['job_description']
#             )
#             response = llm.invoke(messages)
#             state['updated_content']['honors'] = response.content
            
#     except Exception as e:
#         state['error'] = f"Error updating publications/awards/honors: {str(e)}"
    
#     return state

# def generate_final_latex_node(state: ResumeState) -> ResumeState:
#     """Combine all updates into final LaTeX document"""
#     try:
#         final_latex = state['original_latex']
        
#         # Replace each updated section
#         for section_name, new_content in state['updated_content'].items():
#             final_latex = replace_section_in_latex(final_latex, section_name.capitalize(), new_content)
        
#         state['final_latex'] = final_latex
        
#     except Exception as e:
#         state['error'] = f"Error generating final LaTeX: {str(e)}"
    
#     return state

# # ============================================================================
# # LangGraph Workflow Setup
# # ============================================================================

# def create_resume_workflow():
#     """Create the LangGraph workflow for resume building"""
#     workflow = StateGraph(ResumeState)
    
#     # Add nodes
#     workflow.add_node("parse_resume", parse_resume_node)
#     workflow.add_node("fetch_github", fetch_github_node)
#     workflow.add_node("update_projects", analyze_and_update_projects_node)
#     workflow.add_node("update_publications_awards", update_publications_awards_node)
#     workflow.add_node("generate_final", generate_final_latex_node)
    
#     # Define edges
#     workflow.set_entry_point("parse_resume")
#     workflow.add_edge("parse_resume", "fetch_github")
#     workflow.add_edge("fetch_github", "update_projects")
#     workflow.add_edge("update_projects", "update_publications_awards")
#     workflow.add_edge("update_publications_awards", "generate_final")
#     workflow.add_edge("generate_final", END)
    
#     return workflow.compile()

# # ============================================================================
# # Flask Routes
# # ============================================================================

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'service': 'AI Resume Builder (OpenAI)',
#         'model': 'gpt-4o'
#     })

# @app.route('/api/generate-resume', methods=['POST'])
# def generate_resume():
#     """
#     Main endpoint to generate updated resume
    
#     Expected JSON body:
#     {
#         "latex_resume": "LaTeX content",
#         "job_description": "Job description text",
#         "github_username": "optional_username",
#         "publications": "optional publications text",
#         "awards": "optional awards text",
#         "honors": "optional honors text"
#     }
#     """
#     try:
#         data = request.get_json()
        
#         # Validate required fields
#         if not data.get('latex_resume'):
#             return jsonify({'error': 'LaTeX resume is required'}), 400
        
#         if not data.get('job_description'):
#             return jsonify({'error': 'Job description is required'}), 400
        
#         # Initialize state
#         initial_state: ResumeState = {
#             'original_latex': data['latex_resume'],
#             'job_description': data['job_description'],
#             'github_username': data.get('github_username'),
#             'github_repos': [],
#             'publications': data.get('publications'),
#             'awards': data.get('awards'),
#             'honors': data.get('honors'),
#             'parsed_sections': {},
#             'updated_content': {},
#             'final_latex': '',
#             'error': None
#         }
        
#         # Run the workflow
#         workflow = create_resume_workflow()
#         result = workflow.invoke(initial_state)
        
#         # Check for errors
#         if result.get('error'):
#             return jsonify({'error': result['error']}), 500
        
#         # Return the updated LaTeX
#         return jsonify({
#             'success': True,
#             'updated_latex': result['final_latex'],
#             'github_repos_found': len(result.get('github_repos', [])),
#             'sections_updated': list(result.get('updated_content', {}).keys())
#         })
    
#     except Exception as e:
#         return jsonify({'error': f'Server error: {str(e)}'}), 500

# @app.route('/api/generate-resume-pdf', methods=['POST'])
# def generate_resume_pdf():
#     """
#     Generate updated resume and convert to PDF in one step
#     """
#     try:
#         data = request.get_json()
        
#         # Validate required fields
#         if not data.get('latex_resume'):
#             return jsonify({'error': 'LaTeX resume is required'}), 400
        
#         if not data.get('job_description'):
#             return jsonify({'error': 'Job description is required'}), 400
        
#         # Initialize state
#         initial_state: ResumeState = {
#             'original_latex': data['latex_resume'],
#             'job_description': data['job_description'],
#             'github_username': data.get('github_username'),
#             'github_repos': [],
#             'publications': data.get('publications'),
#             'awards': data.get('awards'),
#             'honors': data.get('honors'),
#             'parsed_sections': {},
#             'updated_content': {},
#             'final_latex': '',
#             'error': None
#         }
        
#         # Run the workflow
#         workflow = create_resume_workflow()
#         result = workflow.invoke(initial_state)
        
#         # Check for errors
#         if result.get('error'):
#             return jsonify({'error': result['error']}), 500
        
#         # Convert to PDF using latex.py functionality
#         updated_latex = result['final_latex']
        
#         # Create temporary directory
#         temp_dir = tempfile.mkdtemp()
        
#         try:
#             # File paths
#             tex_file = os.path.join(temp_dir, 'resume.tex')
#             pdf_file = os.path.join(temp_dir, 'resume.pdf')
            
#             # Write LaTeX content to file
#             with open(tex_file, 'w', encoding='utf-8') as f:
#                 f.write(updated_latex)
            
#             # Compile LaTeX to PDF using pdflatex
#             import subprocess
#             for _ in range(2):
#                 result = subprocess.run(
#                     ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
#                     capture_output=True,
#                     text=True,
#                     timeout=30
#                 )
            
#             # Check if PDF was generated
#             if not os.path.exists(pdf_file):
#                 error_log = result.stderr if result.stderr else result.stdout
#                 return jsonify({
#                     'error': 'Failed to compile LaTeX to PDF',
#                     'details': error_log
#                 }), 500
            
#             # Send PDF file
#             return send_file(
#                 pdf_file,
#                 mimetype='application/pdf',
#                 as_attachment=True,
#                 download_name='updated_resume.pdf'
#             )
        
#         finally:
#             # Cleanup temporary directory
#             try:
#                 shutil.rmtree(temp_dir)
#             except:
#                 pass
    
#     except Exception as e:
#         return jsonify({'error': f'Server error: {str(e)}'}), 500

# @app.route('/api/preview-github-repos', methods=['POST'])
# def preview_github_repos():
#     """
#     Preview GitHub repositories for a given username
    
#     Expected JSON body:
#     {
#         "github_username": "username"
#     }
#     """
#     try:
#         data = request.get_json()
        
#         if not data.get('github_username'):
#             return jsonify({'error': 'GitHub username is required'}), 400
        
#         repos = fetch_github_repositories(data['github_username'], GITHUB_TOKEN)
        
#         return jsonify({
#             'success': True,
#             'username': data['github_username'],
#             'repositories': repos,
#             'total_count': len(repos)
#         })
    
#     except Exception as e:
#         return jsonify({'error': f'Error fetching GitHub repos: {str(e)}'}), 500

# @app.route('/api/analyze-job-match', methods=['POST'])
# def analyze_job_match():
#     """
#     Analyze how well projects match a job description
    
#     Expected JSON body:
#     {
#         "github_username": "username",
#         "job_description": "job description text"
#     }
#     """
#     try:
#         data = request.get_json()
        
#         if not data.get('github_username'):
#             return jsonify({'error': 'GitHub username is required'}), 400
        
#         if not data.get('job_description'):
#             return jsonify({'error': 'Job description is required'}), 400
        
#         # Fetch repos
#         repos = fetch_github_repositories(data['github_username'], GITHUB_TOKEN)
        
#         # Use LLM to analyze match
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", """You are an expert career advisor. Analyze GitHub repositories 
# and rate their relevance to a job description. For each project, provide:
# 1. Relevance score (0-10)
# 2. Matching skills/technologies
# 3. Brief explanation of relevance

# Return as JSON array."""),
#             ("human", """
# Job Description:
# {job_desc}

# GitHub Repositories:
# {repos}

# Analyze which projects are most relevant and why.
# """)
#         ])
        
#         messages = prompt.format_messages(
#             job_desc=data['job_description'],
#             repos=str(repos)
#         )
#         response = llm.invoke(messages)
        
#         return jsonify({
#             'success': True,
#             'analysis': response.content,
#             'repositories_analyzed': len(repos)
#         })
    
#     except Exception as e:
#         return jsonify({'error': f'Error analyzing job match: {str(e)}'}), 500

# @app.route('/api/test-latex-parsing', methods=['POST'])
# def test_latex_parsing():
#     """
#     Test endpoint to see how LaTeX resume is parsed
#     """
#     try:
#         data = request.get_json()
        
#         if not data.get('latex_resume'):
#             return jsonify({'error': 'LaTeX resume is required'}), 400
        
#         sections = parse_latex_resume(data['latex_resume'])
        
#         # Return section names and first 100 chars of each
#         preview = {}
#         for section_name, content in sections.items():
#             if section_name != 'raw_content':
#                 preview[section_name] = content[:100] + '...' if len(content) > 100 else content
        
#         return jsonify({
#             'success': True,
#             'sections_found': list(preview.keys()),
#             'preview': preview
#         })
    
#     except Exception as e:
#         return jsonify({'error': f'Error parsing LaTeX: {str(e)}'}), 500

# # ============================================================================
# # Main
# # ============================================================================

# if __name__ == '__main__':
#     # Check for required environment variables
#     if not OPENAI_API_KEY:
#         print("WARNING: OPENAI_API_KEY not set. Please set it as an environment variable.")
#         print("Export it: export OPENAI_API_KEY='your-api-key-here'")
    
#     print("=" * 60)
#     print("AI Resume Builder API (OpenAI)")
#     print("=" * 60)
#     print(f"Model: gpt-4o")
#     print(f"Port: 5001")
#     print("=" * 60)
    
#     app.run(debug=True, port=5001, host='0.0.0.0')
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import re
import requests
from typing import Dict, List, Optional
import tempfile
import shutil
from pathlib import Path

# Import functions from existing files
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# LangChain/LangGraph imports for OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

app = Flask(__name__)
CORS(app)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Set your API key
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')  # Optional: for higher rate limits

# Initialize LLM with OpenAI
llm = ChatOpenAI(
    model="gpt-4o",  # You can also use "gpt-4-turbo", "gpt-4", or "gpt-3.5-turbo"
    api_key=OPENAI_API_KEY,
    temperature=0.7
)

# ============================================================================
# State Definition for LangGraph
# ============================================================================

class ResumeState(TypedDict):
    original_latex: str
    job_description: str
    github_username: Optional[str]
    github_repos: List[Dict]
    publications: Optional[str]
    awards: Optional[str]
    honors: Optional[str]
    parsed_sections: Dict
    updated_content: Dict
    final_latex: str
    error: Optional[str]

# ============================================================================
# GitHub Integration Functions
# ============================================================================

def fetch_github_repositories(username: str, token: Optional[str] = None) -> List[Dict]:
    """
    Fetch user's GitHub repositories
    """
    try:
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        
        url = f'https://api.github.com/users/{username}/repos'
        response = requests.get(
            url,
            headers=headers,
            params={'per_page': 100, 'sort': 'updated', 'type': 'owner'}
        )
        response.raise_for_status()
        
        repos = response.json()
        
        # Get detailed info for each repo
        repo_details = []
        for repo in repos[:20]:  # Limit to top 20 most recent
            repo_info = {
                'name': repo['name'],
                'description': repo.get('description', ''),
                'language': repo.get('language', ''),
                'stars': repo.get('stargazers_count', 0),
                'forks': repo.get('forks_count', 0),
                'url': repo['html_url'],
                'topics': repo.get('topics', []),
                'created_at': repo.get('created_at', ''),
                'updated_at': repo.get('updated_at', ''),
            }
            
            # Try to get README
            try:
                readme_url = f"https://api.github.com/repos/{username}/{repo['name']}/readme"
                readme_resp = requests.get(readme_url, headers=headers)
                if readme_resp.status_code == 200:
                    readme_data = readme_resp.json()
                    # Get raw content
                    content_resp = requests.get(readme_data['download_url'])
                    if content_resp.status_code == 200:
                        repo_info['readme'] = content_resp.text[:1000]  # First 1000 chars
            except:
                pass
            
            repo_details.append(repo_info)
        
        return repo_details
    
    except Exception as e:
        print(f"Error fetching GitHub repos: {str(e)}")
        return []

# ============================================================================
# LaTeX Parsing Functions
# ============================================================================

def parse_latex_resume(latex_content: str) -> Dict:
    """
    Parse LaTeX resume to extract sections
    """
    sections = {
        'projects': '',
        'publications': '',
        'awards': '',
        'honors': '',
        'experience': '',
        'education': '',
        'skills': '',
        'raw_content': latex_content
    }
    
    # Find sections using common LaTeX section markers
    section_patterns = {
        'projects': r'\\section\*?{[Pp]rojects?}(.*?)(?=\\section|\Z)',
        'publications': r'\\section\*?{[Pp]ublications?}(.*?)(?=\\section|\Z)',
        'awards': r'\\section\*?{[Aa]wards?}(.*?)(?=\\section|\Z)',
        'honors': r'\\section\*?{[Hh]onors?}(.*?)(?=\\section|\Z)',
        'experience': r'\\section\*?{[Ee]xperience}(.*?)(?=\\section|\Z)',
        'education': r'\\section\*?{[Ee]ducation}(.*?)(?=\\section|\Z)',
        'skills': r'\\section\*?{[Ss]kills?}(.*?)(?=\\section|\Z)',
    }
    
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, latex_content, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section_name] = match.group(0)
    
    return sections

def replace_section_in_latex(original_latex: str, section_name: str, new_content: str) -> str:
    """
    Replace a specific section in LaTeX while preserving template structure
    
    FIXED: Uses string slicing instead of re.sub() to avoid issues with 
    backslashes in LaTeX content being interpreted as regex escape sequences
    """
    # Escape special regex characters in section_name for pattern matching
    escaped_section_name = re.escape(section_name)
    
    # Find the section - match both \section and \section*
    pattern = rf'(\\section\*?{{{escaped_section_name}}})(.*?)(?=\\section|\Z)'
    
    # Check if section exists
    match = re.search(pattern, original_latex, re.DOTALL | re.IGNORECASE)
    
    if match:
        # Get the start and end positions of the match
        start = match.start()
        end = match.end()
        section_header = match.group(1)
        
        # Build replacement string
        replacement = f"{section_header}\n{new_content}\n"
        
        # Use string slicing instead of re.sub to avoid escape sequence issues
        # This is crucial for LaTeX content which contains many backslashes
        updated_latex = original_latex[:start] + replacement + original_latex[end:]
        return updated_latex
    else:
        # Section doesn't exist, append it before \end{document}
        end_doc_pattern = r'\\end\{document\}'
        match = re.search(end_doc_pattern, original_latex)
        
        if match:
            pos = match.start()
            new_section = f"\n\\section{{{section_name}}}\n{new_content}\n\n"
            updated_latex = original_latex[:pos] + new_section + original_latex[pos:]
            return updated_latex
        else:
            # If no \end{document}, just append at the end
            new_section = f"\n\\section{{{section_name}}}\n{new_content}\n"
            return original_latex + new_section

# ============================================================================
# LangGraph Node Functions
# ============================================================================

def parse_resume_node(state: ResumeState) -> ResumeState:
    """Parse the original LaTeX resume into sections"""
    try:
        sections = parse_latex_resume(state['original_latex'])
        state['parsed_sections'] = sections
        return state
    except Exception as e:
        state['error'] = f"Error parsing resume: {str(e)}"
        return state

def fetch_github_node(state: ResumeState) -> ResumeState:
    """Fetch GitHub repositories if username provided"""
    if state.get('github_username'):
        try:
            repos = fetch_github_repositories(state['github_username'], GITHUB_TOKEN)
            state['github_repos'] = repos
        except Exception as e:
            print(f"Warning: Could not fetch GitHub repos: {str(e)}")
            state['github_repos'] = []
    else:
        state['github_repos'] = []
    
    return state

def analyze_and_update_projects_node(state: ResumeState) -> ResumeState:
    """Use LLM to select and format relevant projects based on job description"""
    try:
        job_desc = state['job_description']
        repos = state['github_repos']
        current_projects = state['parsed_sections'].get('projects', '')
        
        # Create prompt for LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert resume writer specializing in LaTeX formatting. 
Your task is to select and format the most relevant projects for a job application based on:
1. The job description
2. GitHub repositories
3. Current projects in the resume

Follow these guidelines:
- Select 3-5 most relevant projects that match the job requirements
- Maintain the EXACT LaTeX formatting style from the original resume
- Highlight technical skills and technologies mentioned in the job description
- Include quantifiable achievements where possible
- Keep the same LaTeX environment structure (itemize, description, etc.)
- DO NOT change LaTeX commands or document structure
- Output ONLY the LaTeX code for the projects section content (not including \\section header)
- Ensure all backslashes are properly formatted for LaTeX"""),
            ("human", """
Job Description:
{job_desc}

GitHub Repositories:
{repos}

Current Projects Section:
{current_projects}

Generate an updated projects section in LaTeX format that highlights the most relevant projects for this job.
Maintain the exact same LaTeX formatting style as the current projects section.
Output ONLY the content (no section header).
""")
        ])
        
        messages = prompt.format_messages(
            job_desc=job_desc,
            repos=str(repos),
            current_projects=current_projects
        )
        response = llm.invoke(messages)
        updated_projects = response.content
        
        # Clean up any markdown code blocks if present
        updated_projects = updated_projects.replace('```latex', '').replace('```', '').strip()
        
        if 'updated_content' not in state:
            state['updated_content'] = {}
        state['updated_content']['projects'] = updated_projects
        
    except Exception as e:
        state['error'] = f"Error updating projects: {str(e)}"
    
    return state

def update_publications_awards_node(state: ResumeState) -> ResumeState:
    """Update publications, awards, and honors sections"""
    try:
        if 'updated_content' not in state:
            state['updated_content'] = {}
        
        # Get current sections
        current_publications = state['parsed_sections'].get('publications', '')
        current_awards = state['parsed_sections'].get('awards', '')
        current_honors = state['parsed_sections'].get('honors', '')
        
        # Update publications if provided
        if state.get('publications'):
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert at formatting publications in LaTeX for resumes.
Maintain the EXACT LaTeX formatting style from the original resume.
Output ONLY the LaTeX code for the content (not including \\section header).
Ensure all backslashes are properly formatted for LaTeX."""),
                ("human", """
Current Publications Section:
{current_publications}

New Publications to Add:
{new_publications}

Job Description (for relevance):
{job_desc}

Generate an updated publications section in LaTeX format, prioritizing those most relevant to the job.
Maintain the exact same LaTeX formatting style.
Output ONLY the content.
""")
            ])
            
            messages = prompt.format_messages(
                current_publications=current_publications,
                new_publications=state['publications'],
                job_desc=state['job_description']
            )
            response = llm.invoke(messages)
            cleaned_content = response.content.replace('```latex', '').replace('```', '').strip()
            state['updated_content']['publications'] = cleaned_content
        
        # Update awards if provided
        if state.get('awards'):
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert at formatting awards in LaTeX for resumes.
Maintain the EXACT LaTeX formatting style from the original resume.
Output ONLY the LaTeX code for the content (not including \\section header).
Ensure all backslashes are properly formatted for LaTeX."""),
                ("human", """
Current Awards Section:
{current_awards}

New Awards to Add:
{new_awards}

Job Description (for relevance):
{job_desc}

Generate an updated awards section in LaTeX format, prioritizing those most relevant to the job.
Maintain the exact same LaTeX formatting style.
Output ONLY the content.
""")
            ])
            
            messages = prompt.format_messages(
                current_awards=current_awards,
                new_awards=state['awards'],
                job_desc=state['job_description']
            )
            response = llm.invoke(messages)
            cleaned_content = response.content.replace('```latex', '').replace('```', '').strip()
            state['updated_content']['awards'] = cleaned_content
        
        # Update honors if provided
        if state.get('honors'):
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert at formatting honors in LaTeX for resumes.
Maintain the EXACT LaTeX formatting style from the original resume.
Output ONLY the LaTeX code for the content (not including \\section header).
Ensure all backslashes are properly formatted for LaTeX."""),
                ("human", """
Current Honors Section:
{current_honors}

New Honors to Add:
{new_honors}

Job Description (for relevance):
{job_desc}

Generate an updated honors section in LaTeX format, prioritizing those most relevant to the job.
Maintain the exact same LaTeX formatting style.
Output ONLY the content.
""")
            ])
            
            messages = prompt.format_messages(
                current_honors=current_honors,
                new_honors=state['honors'],
                job_desc=state['job_description']
            )
            response = llm.invoke(messages)
            cleaned_content = response.content.replace('```latex', '').replace('```', '').strip()
            state['updated_content']['honors'] = cleaned_content
            
    except Exception as e:
        state['error'] = f"Error updating publications/awards/honors: {str(e)}"
    
    return state

def generate_final_latex_node(state: ResumeState) -> ResumeState:
    """Combine all updates into final LaTeX document"""
    try:
        final_latex = state['original_latex']
        
        # Replace each updated section
        for section_name, new_content in state['updated_content'].items():
            final_latex = replace_section_in_latex(final_latex, section_name.capitalize(), new_content)
        
        state['final_latex'] = final_latex
        
    except Exception as e:
        state['error'] = f"Error generating final LaTeX: {str(e)}"
        import traceback
        state['error'] += f"\n{traceback.format_exc()}"
    
    return state

# ============================================================================
# LangGraph Workflow Setup
# ============================================================================

def create_resume_workflow():
    """Create the LangGraph workflow for resume building"""
    workflow = StateGraph(ResumeState)
    
    # Add nodes
    workflow.add_node("parse_resume", parse_resume_node)
    workflow.add_node("fetch_github", fetch_github_node)
    workflow.add_node("update_projects", analyze_and_update_projects_node)
    workflow.add_node("update_publications_awards", update_publications_awards_node)
    workflow.add_node("generate_final", generate_final_latex_node)
    
    # Define edges
    workflow.set_entry_point("parse_resume")
    workflow.add_edge("parse_resume", "fetch_github")
    workflow.add_edge("fetch_github", "update_projects")
    workflow.add_edge("update_projects", "update_publications_awards")
    workflow.add_edge("update_publications_awards", "generate_final")
    workflow.add_edge("generate_final", END)
    
    return workflow.compile()

# ============================================================================
# Flask Routes
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Resume Builder (OpenAI)',
        'model': 'gpt-4o'
    })

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    """
    Main endpoint to generate updated resume
    
    Expected JSON body:
    {
        "latex_resume": "LaTeX content",
        "job_description": "Job description text",
        "github_username": "optional_username",
        "publications": "optional publications text",
        "awards": "optional awards text",
        "honors": "optional honors text"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('latex_resume'):
            return jsonify({'error': 'LaTeX resume is required'}), 400
        
        if not data.get('job_description'):
            return jsonify({'error': 'Job description is required'}), 400
        
        # Initialize state
        initial_state: ResumeState = {
            'original_latex': data['latex_resume'],
            'job_description': data['job_description'],
            'github_username': data.get('github_username'),
            'github_repos': [],
            'publications': data.get('publications'),
            'awards': data.get('awards'),
            'honors': data.get('honors'),
            'parsed_sections': {},
            'updated_content': {},
            'final_latex': '',
            'error': None
        }
        
        # Run the workflow
        workflow = create_resume_workflow()
        result = workflow.invoke(initial_state)
        
        # Check for errors
        if result.get('error'):
            return jsonify({'error': result['error']}), 500
        
        # Return the updated LaTeX
        return jsonify({
            'success': True,
            'updated_latex': result['final_latex'],
            'github_repos_found': len(result.get('github_repos', [])),
            'sections_updated': list(result.get('updated_content', {}).keys())
        })
    
    except Exception as e:
        import traceback
        return jsonify({
            'error': f'Server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/generate-resume-pdf', methods=['POST'])
def generate_resume_pdf():
    """
    Generate updated resume and convert to PDF in one step
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('latex_resume'):
            return jsonify({'error': 'LaTeX resume is required'}), 400
        
        if not data.get('job_description'):
            return jsonify({'error': 'Job description is required'}), 400
        
        # Initialize state
        initial_state: ResumeState = {
            'original_latex': data['latex_resume'],
            'job_description': data['job_description'],
            'github_username': data.get('github_username'),
            'github_repos': [],
            'publications': data.get('publications'),
            'awards': data.get('awards'),
            'honors': data.get('honors'),
            'parsed_sections': {},
            'updated_content': {},
            'final_latex': '',
            'error': None
        }
        
        # Run the workflow
        workflow = create_resume_workflow()
        result = workflow.invoke(initial_state)
        
        # Check for errors
        if result.get('error'):
            return jsonify({'error': result['error']}), 500
        
        # Convert to PDF using latex.py functionality
        updated_latex = result['final_latex']
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # File paths
            tex_file = os.path.join(temp_dir, 'resume.tex')
            pdf_file = os.path.join(temp_dir, 'resume.pdf')
            
            # Write LaTeX content to file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(updated_latex)
            
            # Compile LaTeX to PDF using pdflatex
            import subprocess
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            # Check if PDF was generated
            if not os.path.exists(pdf_file):
                error_log = result.stderr if result.stderr else result.stdout
                return jsonify({
                    'error': 'Failed to compile LaTeX to PDF',
                    'details': error_log
                }), 500
            
            # Send PDF file
            return send_file(
                pdf_file,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='updated_resume.pdf'
            )
        
        finally:
            # Cleanup temporary directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    except Exception as e:
        import traceback
        return jsonify({
            'error': f'Server error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/preview-github-repos', methods=['POST'])
def preview_github_repos():
    """
    Preview GitHub repositories for a given username
    
    Expected JSON body:
    {
        "github_username": "username"
    }
    """
    try:
        data = request.get_json()
        
        if not data.get('github_username'):
            return jsonify({'error': 'GitHub username is required'}), 400
        
        repos = fetch_github_repositories(data['github_username'], GITHUB_TOKEN)
        
        return jsonify({
            'success': True,
            'username': data['github_username'],
            'repositories': repos,
            'total_count': len(repos)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error fetching GitHub repos: {str(e)}'}), 500

@app.route('/api/analyze-job-match', methods=['POST'])
def analyze_job_match():
    """
    Analyze how well projects match a job description
    
    Expected JSON body:
    {
        "github_username": "username",
        "job_description": "job description text"
    }
    """
    try:
        data = request.get_json()
        
        if not data.get('github_username'):
            return jsonify({'error': 'GitHub username is required'}), 400
        
        if not data.get('job_description'):
            return jsonify({'error': 'Job description is required'}), 400
        
        # Fetch repos
        repos = fetch_github_repositories(data['github_username'], GITHUB_TOKEN)
        
        # Use LLM to analyze match
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert career advisor. Analyze GitHub repositories 
and rate their relevance to a job description. For each project, provide:
1. Relevance score (0-10)
2. Matching skills/technologies
3. Brief explanation of relevance

Return as JSON array."""),
            ("human", """
Job Description:
{job_desc}

GitHub Repositories:
{repos}

Analyze which projects are most relevant and why.
""")
        ])
        
        messages = prompt.format_messages(
            job_desc=data['job_description'],
            repos=str(repos)
        )
        response = llm.invoke(messages)
        
        return jsonify({
            'success': True,
            'analysis': response.content,
            'repositories_analyzed': len(repos)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing job match: {str(e)}'}), 500

@app.route('/api/test-latex-parsing', methods=['POST'])
def test_latex_parsing():
    """
    Test endpoint to see how LaTeX resume is parsed
    """
    try:
        data = request.get_json()
        
        if not data.get('latex_resume'):
            return jsonify({'error': 'LaTeX resume is required'}), 400
        
        sections = parse_latex_resume(data['latex_resume'])
        
        # Return section names and first 100 chars of each
        preview = {}
        for section_name, content in sections.items():
            if section_name != 'raw_content':
                preview[section_name] = content[:100] + '...' if len(content) > 100 else content
        
        return jsonify({
            'success': True,
            'sections_found': list(preview.keys()),
            'preview': preview
        })
    
    except Exception as e:
        return jsonify({'error': f'Error parsing LaTeX: {str(e)}'}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Check for required environment variables
    if not OPENAI_API_KEY:
        print("WARNING: OPENAI_API_KEY not set. Please set it as an environment variable.")
        print("Export it: export OPENAI_API_KEY='your-api-key-here'")
    
    print("=" * 60)
    print("AI Resume Builder API (OpenAI) - FIXED VERSION")
    print("=" * 60)
    print(f"Model: gpt-4o")
    print(f"Port: 5001")
    print("Fixed: Regex escape sequence issue with LaTeX content")
    print("=" * 60)
    
    app.run(debug=True, port=5001, host='0.0.0.0')