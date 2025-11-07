# # import os
# # import google.generativeai as genai
# # from dotenv import load_dotenv
# # import PyPDF2

# # class CareerPathPlanner:
# #     def __init__(self):
# #         # Load environment variables from .env file
# #         load_dotenv()
        
# #         # Configure Gemini API
# #         api_key = os.getenv('GEMINI_API_KEY')
# #         if not api_key:
# #             raise ValueError("GEMINI_API_KEY not found in .env file")
        
# #         genai.configure(api_key=api_key)
# #         self.model = genai.GenerativeModel('gemini-pro')
    
# #     def extract_text_from_pdf(self, pdf_path):
# #         """Extract text content from PDF resume"""
# #         try:
# #             with open(pdf_path, 'rb') as file:
# #                 pdf_reader = PyPDF2.PdfReader(file)
# #                 text = ""
# #                 for page in pdf_reader.pages:
# #                     text += page.extract_text()
# #                 return text
# #         except Exception as e:
# #             print(f"Error reading PDF: {e}")
# #             return None
    
# #     def collect_user_info(self):
# #         """Collect information from user"""
# #         print("\n" + "="*60)
# #         print("CAREER PATH PLANNER".center(60))
# #         print("="*60 + "\n")
        
# #         user_data = {}
        
# #         # Basic Information
# #         print("📚 ACADEMIC INFORMATION")
# #         print("-" * 60)
# #         user_data['college'] = input("College/University Name: ").strip()
# #         user_data['branch'] = input("Branch/Major (e.g., CSE, ECE, IT): ").strip()
# #         user_data['cgpa'] = input("CGPA/Percentage: ").strip()
        
# #         # Skills
# #         print("\n💻 SKILLS & INTERESTS")
# #         print("-" * 60)
# #         user_data['skills'] = input("Technical Skills (comma-separated): ").strip()
# #         user_data['interests'] = input("Areas of Interest (comma-separated): ").strip()
        
# #         # Experience
# #         print("\n🔨 EXPERIENCE & PROJECTS")
# #         print("-" * 60)
# #         user_data['projects'] = input("Projects Done (brief description): ").strip()
        
# #         # Career Goals
# #         print("\n🎯 CAREER GOALS")
# #         print("-" * 60)
# #         user_data['desired_role'] = input("Desired Job Role: ").strip()
        
# #         # Additional Information
# #         print("\n📝 ADDITIONAL INFORMATION (Optional)")
# #         print("-" * 60)
# #         user_data['additional_info'] = input("Any other relevant information: ").strip()
        
# #         # Resume Upload
# #         print("\n📄 RESUME (Optional)")
# #         print("-" * 60)
# #         resume_path = input("Enter resume PDF path (or press Enter to skip): ").strip()
        
# #         if resume_path and os.path.exists(resume_path):
# #             print("Extracting resume information...")
# #             resume_text = self.extract_text_from_pdf(resume_path)
# #             if resume_text:
# #                 user_data['resume_content'] = resume_text
# #                 print("✅ Resume processed successfully!")
# #             else:
# #                 print("⚠️  Could not extract text from resume")
        
# #         return user_data
    
# #     def generate_career_path(self, user_data):
# #         """Generate personalized career path using Gemini API"""
        
# #         # Construct detailed prompt
# #         prompt = f"""
# # You are an expert career counselor and mentor. Based on the following information about a student/professional, 
# # create a comprehensive and personalized career roadmap.

# # STUDENT/PROFESSIONAL PROFILE:
# # - College/University: {user_data.get('college', 'Not provided')}
# # - Branch/Major: {user_data.get('branch', 'Not provided')}
# # - CGPA/Grade: {user_data.get('cgpa', 'Not provided')}
# # - Technical Skills: {user_data.get('skills', 'Not provided')}
# # - Areas of Interest: {user_data.get('interests', 'Not provided')}
# # - Projects Completed: {user_data.get('projects', 'Not provided')}
# # - Desired Job Role: {user_data.get('desired_role', 'Not provided')}
# # - Additional Information: {user_data.get('additional_info', 'Not provided')}

# # {f"RESUME HIGHLIGHTS: {user_data.get('resume_content', '')[:1000]}" if 'resume_content' in user_data else ''}

# # PLEASE PROVIDE A DETAILED CAREER ROADMAP WITH THE FOLLOWING SECTIONS:

# # ## 1. IMMEDIATE ACTION ITEMS (Next 1-3 months)
# # • List specific, actionable steps they should take immediately
# # • Include skill development priorities
# # • Focus on quick wins

# # ## 2. SHORT-TERM GOALS (3-6 months)
# # • Technical skills to master
# # • Projects to build
# # • Certifications to pursue
# # • Networking strategies

# # ## 3. MEDIUM-TERM ROADMAP (6-12 months)
# # • Advanced skill development
# # • Portfolio building
# # • Interview preparation
# # • Job application strategies

# # ## 4. LONG-TERM CAREER PATH (1-3 years)
# # • Career progression trajectory
# # • Specialization recommendations
# # • Leadership development
# # • Industry positioning

# # ## 5. RECOMMENDED COURSES & RESOURCES
# # For each recommendation, provide:
# # • Course Name
# # • Platform/Provider
# # • Direct URL (if available)
# # • Why this course is relevant
# # • Estimated time commitment

# # Focus on courses from platforms like:
# # - Coursera (https://www.coursera.org)
# # - edX (https://www.edx.org)
# # - Udemy (https://www.udemy.com)
# # - freeCodeCamp (https://www.freecodecamp.org)
# # - LinkedIn Learning (https://www.linkedin.com/learning)
# # - YouTube channels
# # - Official documentation

# # ## 6. SKILLS GAP ANALYSIS
# # • Skills they have vs. skills needed for desired role
# # • Priority order for learning
# # • Estimated time to become job-ready

# # ## 7. PROJECT IDEAS
# # • 3-5 specific project ideas that align with their career goals
# # • Brief description of each project
# # • Technologies to use

# # ## 8. NETWORKING & COMMUNITY
# # • Communities to join
# # • Events to attend
# # • How to build their personal brand

# # ## 9. JOB SEARCH STRATEGY
# # • Where to look for opportunities
# # • How to optimize their resume
# # • Interview preparation tips

# # ## 10. ADDITIONAL RECOMMENDATIONS
# # • Books to read
# # • Podcasts/YouTube channels to follow
# # • Mentorship opportunities

# # Format everything in clear bullet points with specific, actionable advice.
# # Be encouraging but realistic about timelines and effort required.
# # """
        
# #         print("\n🤖 Generating personalized career roadmap...")
# #         print("⏳ This may take a moment...\n")
        
# #         try:
# #             response = self.model.generate_content(prompt)
# #             return response.text
# #         except Exception as e:
# #             return f"Error generating career path: {e}"
    
# #     def save_roadmap(self, roadmap, user_data):
# #         """Save the generated roadmap to a file"""
# #         filename = f"career_roadmap_{user_data.get('college', 'user').replace(' ', '_')}.txt"
        
# #         with open(filename, 'w', encoding='utf-8') as f:
# #             f.write("="*80 + "\n")
# #             f.write("PERSONALIZED CAREER ROADMAP\n")
# #             f.write("="*80 + "\n\n")
# #             f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
# #             f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
# #             f.write(f"Branch: {user_data.get('branch', 'N/A')}\n")
# #             f.write("\n" + "="*80 + "\n\n")
# #             f.write(roadmap)
        
# #         return filename
    
# #     def run(self):
# #         """Main execution flow"""
# #         try:
# #             # Collect user information
# #             user_data = self.collect_user_info()
            
# #             # Generate career path
# #             roadmap = self.generate_career_path(user_data)
            
# #             # Display roadmap
# #             print("\n" + "="*80)
# #             print("YOUR PERSONALIZED CAREER ROADMAP")
# #             print("="*80 + "\n")
# #             print(roadmap)
            
# #             # Save to file
# #             filename = self.save_roadmap(roadmap, user_data)
# #             print(f"\n✅ Career roadmap saved to: {filename}")
            
# #         except KeyboardInterrupt:
# #             print("\n\n⚠️  Process interrupted by user")
# #         except Exception as e:
# #             print(f"\n❌ Error: {e}")


# # if __name__ == "__main__":
# #     planner = CareerPathPlanner()
# #     planner.run()



# import os
# import google.generativeai as genai
# from dotenv import load_dotenv
# import PyPDF2

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
    
#     def extract_text_from_pdf(self, pdf_path):
#         """Extract text content from PDF resume"""
#         try:
#             with open(pdf_path, 'rb') as file:
#                 pdf_reader = PyPDF2.PdfReader(file)
#                 text = ""
#                 for page in pdf_reader.pages:
#                     text += page.extract_text()
#                 return text
#         except Exception as e:
#             print(f"Error reading PDF: {e}")
#             return None
    
#     def collect_user_info(self):
#         """Collect information from user"""
#         print("\n" + "="*60)
#         print("CAREER PATH PLANNER".center(60))
#         print("="*60 + "\n")
        
#         user_data = {}
        
#         # Basic Information
#         print("📚 ACADEMIC INFORMATION")
#         print("-" * 60)
#         user_data['college'] = input("College/University Name: ").strip()
#         user_data['branch'] = input("Branch/Major (e.g., CSE, ECE, IT): ").strip()
#         user_data['cgpa'] = input("CGPA/Percentage: ").strip()
        
#         # Skills
#         print("\n💻 SKILLS & INTERESTS")
#         print("-" * 60)
#         user_data['skills'] = input("Technical Skills (comma-separated): ").strip()
#         user_data['interests'] = input("Areas of Interest (comma-separated): ").strip()
        
#         # Experience
#         print("\n🔨 EXPERIENCE & PROJECTS")
#         print("-" * 60)
#         user_data['projects'] = input("Projects Done (brief description): ").strip()
        
#         # Career Goals
#         print("\n🎯 CAREER GOALS")
#         print("-" * 60)
#         user_data['desired_role'] = input("Desired Job Role: ").strip()
        
#         # Additional Information
#         print("\n📝 ADDITIONAL INFORMATION (Optional)")
#         print("-" * 60)
#         user_data['additional_info'] = input("Any other relevant information: ").strip()
        
#         # Resume Upload
#         print("\n📄 RESUME (Optional)")
#         print("-" * 60)
#         resume_path = input("Enter resume PDF path (or press Enter to skip): ").strip()
        
#         if resume_path and os.path.exists(resume_path):
#             print("Extracting resume information...")
#             resume_text = self.extract_text_from_pdf(resume_path)
#             if resume_text:
#                 user_data['resume_content'] = resume_text
#                 print("✅ Resume processed successfully!")
#             else:
#                 print("⚠️  Could not extract text from resume")
        
#         return user_data
    
#     def generate_career_path(self, user_data):
#         """Generate personalized career path using Gemini API"""
        
#         # Construct detailed prompt
#         prompt = f"""
# You are an expert career counselor and mentor. Based on the following information about a student/professional, 
# create a comprehensive and personalized career roadmap.

# STUDENT/PROFESSIONAL PROFILE:
# - College/University: {user_data.get('college', 'Not provided')}
# - Branch/Major: {user_data.get('branch', 'Not provided')}
# - CGPA/Grade: {user_data.get('cgpa', 'Not provided')}
# - Technical Skills: {user_data.get('skills', 'Not provided')}
# - Areas of Interest: {user_data.get('interests', 'Not provided')}
# - Projects Completed: {user_data.get('projects', 'Not provided')}
# - Desired Job Role: {user_data.get('desired_role', 'Not provided')}
# - Additional Information: {user_data.get('additional_info', 'Not provided')}

# {f"RESUME HIGHLIGHTS: {user_data.get('resume_content', '')[:1000]}" if 'resume_content' in user_data else ''}

# PLEASE PROVIDE A DETAILED CAREER ROADMAP WITH THE FOLLOWING SECTIONS:

# ## 1. IMMEDIATE ACTION ITEMS (Next 1-3 months)
# • List specific, actionable steps they should take immediately
# • Include skill development priorities
# • Focus on quick wins

# ## 2. SHORT-TERM GOALS (3-6 months)
# • Technical skills to master
# • Projects to build
# • Certifications to pursue
# • Networking strategies

# ## 3. MEDIUM-TERM ROADMAP (6-12 months)
# • Advanced skill development
# • Portfolio building
# • Interview preparation
# • Job application strategies

# ## 4. LONG-TERM CAREER PATH (1-3 years)
# • Career progression trajectory
# • Specialization recommendations
# • Leadership development
# • Industry positioning

# ## 5. RECOMMENDED COURSES & RESOURCES
# For each recommendation, provide:
# • Course Name
# • Platform/Provider
# • Direct URL (if available)
# • Why this course is relevant
# • Estimated time commitment

# Focus on courses from platforms like:
# - Coursera (https://www.coursera.org)
# - edX (https://www.edx.org)
# - Udemy (https://www.udemy.com)
# - freeCodeCamp (https://www.freecodecamp.org)
# - LinkedIn Learning (https://www.linkedin.com/learning)
# - YouTube channels
# - Official documentation

# ## 6. SKILLS GAP ANALYSIS
# • Skills they have vs. skills needed for desired role
# • Priority order for learning
# • Estimated time to become job-ready

# ## 7. PROJECT IDEAS
# • 3-5 specific project ideas that align with their career goals
# • Brief description of each project
# • Technologies to use

# ## 8. NETWORKING & COMMUNITY
# • Communities to join
# • Events to attend
# • How to build their personal brand

# ## 9. JOB SEARCH STRATEGY
# • Where to look for opportunities
# • How to optimize their resume
# • Interview preparation tips

# ## 10. ADDITIONAL RECOMMENDATIONS
# • Books to read
# • Podcasts/YouTube channels to follow
# • Mentorship opportunities

# Format everything in clear bullet points with specific, actionable advice.
# Be encouraging but realistic about timelines and effort required.
# """
        
#         print("\n🤖 Generating personalized career roadmap...")
#         print("⏳ This may take a moment...\n")
        
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             return f"Error generating career path: {e}"
    
#     def save_roadmap(self, roadmap, user_data):
#         """Save the generated roadmap to a file"""
#         filename = f"career_roadmap_{user_data.get('college', 'user').replace(' ', '_')}.txt"
        
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write("="*80 + "\n")
#             f.write("PERSONALIZED CAREER ROADMAP\n")
#             f.write("="*80 + "\n\n")
#             f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
#             f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
#             f.write(f"Branch: {user_data.get('branch', 'N/A')}\n")
#             f.write("\n" + "="*80 + "\n\n")
#             f.write(roadmap)
        
#         return filename
    
#     def run(self):
#         """Main execution flow"""
#         try:
#             # Collect user information
#             user_data = self.collect_user_info()
            
#             # Generate career path
#             roadmap = self.generate_career_path(user_data)
            
#             # Display roadmap
#             print("\n" + "="*80)
#             print("YOUR PERSONALIZED CAREER ROADMAP")
#             print("="*80 + "\n")
#             print(roadmap)
            
#             # Save to file
#             filename = self.save_roadmap(roadmap, user_data)
#             print(f"\n✅ Career roadmap saved to: {filename}")
            
#         except KeyboardInterrupt:
#             print("\n\n⚠️  Process interrupted by user")
#         except Exception as e:
#             print(f"\n❌ Error: {e}")
    
#     def run_with_data(self, user_data):
#         """Run the planner with pre-filled data (for testing)"""
#         try:
#             # Generate career path
#             roadmap = self.generate_career_path(user_data)
            
#             # Display roadmap
#             print("\n" + "="*80)
#             print("YOUR PERSONALIZED CAREER ROADMAP")
#             print("="*80 + "\n")
#             print(roadmap)
            
#             # Save to file
#             filename = self.save_roadmap(roadmap, user_data)
#             print(f"\n✅ Career roadmap saved to: {filename}")
            
#             return roadmap, filename
            
#         except Exception as e:
#             print(f"\n❌ Error: {e}")
#             return None, None


# def test_with_sample_data():
#     """Test function with sample data"""
    
#     print("\n" + "="*80)
#     print("TESTING CAREER PATH PLANNER WITH SAMPLE DATA".center(80))
#     print("="*80 + "\n")
    
#     # Sample test data
#     test_data = {
#         'college': 'JNGEC',
#         'branch': 'Computer Science Engineering',
#         'cgpa': '7.6',
#         'skills': 'Python, JavaScript, React, Node.js, SQL, Git,n8n , tensorflow , pytorch',
#         'interests': 'Machine Learning, Cloud Computing,Web Development',
#         'projects': 'E-commerce website using MERN stack, Chatbot using NLP, Data analysis dashboard',
#         'desired_role': 'Full Stack Developer',
#         'additional_info': 'Completed 2 internships, active on GitHub, looking for opportunities in product-based companies'
#     }
    
#     print("📋 Test Data:")
#     print("-" * 80)
#     for key, value in test_data.items():
#         print(f"{key.replace('_', ' ').title()}: {value}")
#     print("-" * 80)
    
#     proceed = input("\n➡️  Proceed with this test data? (y/n): ").strip().lower()
    
#     if proceed == 'y':
#         planner = CareerPathPlanner()
#         roadmap, filename = planner.run_with_data(test_data)
        
#         if roadmap:
#             print("\n✅ Test completed successfully!")
#             print(f"📄 Results saved to: {filename}")
#     else:
#         print("\n❌ Test cancelled")


# def test_interactive_mode():
#     """Run in normal interactive mode"""
#     print("\n" + "="*80)
#     print("INTERACTIVE MODE - ENTER YOUR DATA".center(80))
#     print("="*80 + "\n")
    
#     planner = CareerPathPlanner()
#     planner.run()


# def test_custom_data():
#     """Test with custom data that user provides"""
#     print("\n" + "="*80)
#     print("CUSTOM TEST MODE".center(80))
#     print("="*80 + "\n")
    
#     user_data = {}
    
#     print("Enter your test data (press Enter to skip optional fields):\n")
    
#     user_data['college'] = input("College/University: ").strip() or "Test University"
#     user_data['branch'] = input("Branch/Major: ").strip() or "CSE"
#     user_data['cgpa'] = input("CGPA: ").strip() or "8.0"
#     user_data['skills'] = input("Skills (comma-separated): ").strip() or "Python, Java"
#     user_data['interests'] = input("Interests: ").strip() or "Software Development"
#     user_data['projects'] = input("Projects: ").strip() or "Personal portfolio website"
#     user_data['desired_role'] = input("Desired Role: ").strip() or "Software Engineer"
#     user_data['additional_info'] = input("Additional Info: ").strip() or ""
    
#     print("\n" + "-"*80)
#     print("Test data entered:")
#     for key, value in user_data.items():
#         if value:
#             print(f"  {key}: {value}")
#     print("-"*80)
    
#     planner = CareerPathPlanner()
#     planner.run_with_data(user_data)


# if __name__ == "__main__":
#     print("\n" + "="*80)
#     print("CAREER PATH PLANNER - TEST SUITE".center(80))
#     print("="*80 + "\n")
    
#     print("Choose a test mode:")
#     print("1. Test with sample data (automated)")
#     print("2. Test with custom data (quick entry)")
#     print("3. Interactive mode (full manual entry)")
#     print("4. Exit")
    
#     choice = input("\nEnter your choice (1-4): ").strip()
    
#     if choice == '1':
#         test_with_sample_data()
#     elif choice == '2':
#         test_custom_data()
#     elif choice == '3':
#         test_interactive_mode()
#     elif choice == '4':
#         print("\n👋 Goodbye!")
#     else:
#         print("\n❌ Invalid choice. Please run again and select 1-4.")





import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2

class CareerPathPlanner:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF resume"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def collect_user_info(self):
        """Collect comprehensive information from user"""
        print("\n" + "="*70)
        print("ADVANCED CAREER PATH PLANNER".center(70))
        print("="*70 + "\n")
        
        user_data = {}
        
        # ========== BASIC INFORMATION ==========
        print("📚 ACADEMIC INFORMATION")
        print("-" * 70)
        user_data['college'] = input("College/University Name: ").strip()
        user_data['branch'] = input("Branch/Major (e.g., CSE, ECE, IT): ").strip()
        user_data['cgpa'] = input("CGPA/Percentage: ").strip()
        
        # ========== SKILLS & EXPERIENCE ==========
        print("\n💻 SKILLS & EXPERIENCE")
        print("-" * 70)
        user_data['skills'] = input("Technical Skills (comma-separated): ").strip()
        user_data['interests'] = input("Areas of Interest (comma-separated): ").strip()
        user_data['strengths'] = input("Your Strengths (e.g., problem-solving, communication): ").strip()
        user_data['weaknesses'] = input("Areas to Improve (optional): ").strip()
        
        # ========== CERTIFICATIONS & PROJECTS ==========
        print("\n🏆 CERTIFICATIONS & PROJECTS")
        print("-" * 70)
        user_data['certifications_done'] = input("Certifications Completed (comma-separated, or skip): ").strip()
        user_data['projects'] = input("Projects Done (brief description): ").strip()
        user_data['internship_experience'] = input("Internship Experience (if any): ").strip()
        
        # ========== CAREER GOALS ==========
        print("\n🎯 CAREER GOALS")
        print("-" * 70)
        user_data['desired_role'] = input("Desired Job Role: ").strip()
        user_data['target_industry'] = input("Target Industry/Domain (e.g., AI, Fintech, Web Dev): ").strip()
        
        # ========== WORK PREFERENCES ==========
        print("\n🌍 WORK PREFERENCES")
        print("-" * 70)
        print("Preferred Work Type: 1) Remote  2) On-site  3) Hybrid")
        work_choice = input("Enter choice (1-3): ").strip()
        work_map = {'1': 'Remote', '2': 'On-site', '3': 'Hybrid'}
        user_data['preferred_work_type'] = work_map.get(work_choice, 'Flexible')
        
        # ========== TIME & LEARNING ==========
        print("\n⏰ TIME COMMITMENT & LEARNING STYLE")
        print("-" * 70)
        user_data['available_hours_per_week'] = input("Available Hours Per Week for Learning: ").strip()
        
        print("\nRoadmap Duration Preference:")
        print("1) Short (6 months)  2) Medium (1 year)  3) Long-term (2-3 years)")
        duration_choice = input("Enter choice (1-3): ").strip()
        duration_map = {'1': '6 months', '2': '1 year', '3': '2-3 years'}
        user_data['roadmap_duration'] = duration_map.get(duration_choice, '1 year')
        
        print("\nLearning Style:")
        print("1) Video Courses  2) Project-Based  3) Reading  4) Group Learning  5) Mixed")
        learning_choice = input("Enter choice (1-5): ").strip()
        learning_map = {'1': 'Video Courses', '2': 'Project-Based', '3': 'Reading', 
                       '4': 'Group Learning', '5': 'Mixed'}
        user_data['learning_style'] = learning_map.get(learning_choice, 'Mixed')
        
        # ========== PERSONALITY & BUDGET ==========
        print("\n🧠 PERSONALITY & CONSTRAINTS")
        print("-" * 70)
        print("Personality Type:")
        print("1) Analytical  2) Creative  3) Leader  4) Collaborative  5) Independent")
        personality_choice = input("Enter choice (1-5): ").strip()
        personality_map = {'1': 'Analytical', '2': 'Creative', '3': 'Leader', 
                          '4': 'Collaborative', '5': 'Independent'}
        user_data['personality_type'] = personality_map.get(personality_choice, 'Balanced')
        
        print("\nBudget Preference:")
        print("1) Free Only  2) Affordable (<$50/month)  3) Premium  4) No Constraint")
        budget_choice = input("Enter choice (1-4): ").strip()
        budget_map = {'1': 'Free Only', '2': 'Affordable (<$50/month)', 
                     '3': 'Premium', '4': 'No Constraint'}
        user_data['budget_preference'] = budget_map.get(budget_choice, 'Affordable')
        
        # ========== ROADMAP MODE ==========
        print("\n📋 ROADMAP TYPE")
        print("-" * 70)
        print("1) Short (Quick overview)  2) Detailed (Comprehensive)  3) Executive Summary")
        mode_choice = input("Enter choice (1-3): ").strip()
        mode_map = {'1': 'short', '2': 'detailed', '3': 'executive summary'}
        user_data['mode'] = mode_map.get(mode_choice, 'detailed')
        
        # ========== ADDITIONAL INFO ==========
        print("\n📝 ADDITIONAL INFORMATION (Optional)")
        print("-" * 70)
        user_data['additional_info'] = input("Any other relevant information: ").strip()
        
        # ========== RESUME UPLOAD ==========
        print("\n📄 RESUME (Optional)")
        print("-" * 70)
        resume_path = input("Enter resume PDF path (or press Enter to skip): ").strip()
        
        if resume_path and os.path.exists(resume_path):
            print("Extracting resume information...")
            resume_text = self.extract_text_from_pdf(resume_path)
            if resume_text:
                user_data['resume_content'] = resume_text
                print("✅ Resume processed successfully!")
            else:
                print("⚠️  Could not extract text from resume")
        
        return user_data
    
    def generate_career_path(self, user_data):
        """Generate personalized career path using Gemini API with enhanced prompt"""
        
        # Construct enhanced detailed prompt
        prompt = f"""
You are an expert AI career mentor and roadmap planner.

Your task is to design a **personalized, step-by-step career roadmap** based on the following profile:

STUDENT/PROFESSIONAL DETAILS:
- College/University: {user_data.get('college', 'Not provided')}
- Branch/Major: {user_data.get('branch', 'Not provided')}
- CGPA/Grade: {user_data.get('cgpa', 'Not provided')}
- Technical Skills: {user_data.get('skills', 'Not provided')}
- Interests: {user_data.get('interests', 'Not provided')}
- Strengths: {user_data.get('strengths', 'Not provided')}
- Weaknesses: {user_data.get('weaknesses', 'Not provided')}
- Projects Done: {user_data.get('projects', 'Not provided')}
- Certifications Done: {user_data.get('certifications_done', 'Not provided')}
- Internship Experience: {user_data.get('internship_experience', 'Not provided')}
- Preferred Work Type: {user_data.get('preferred_work_type', 'Not provided')}
- Desired Job Role: {user_data.get('desired_role', 'Not provided')}
- Target Industry / Domain: {user_data.get('target_industry', 'Not provided')}
- Available Hours Per Week: {user_data.get('available_hours_per_week', 'Not provided')}
- Roadmap Duration: {user_data.get('roadmap_duration', '1 year')}
- Budget Preference: {user_data.get('budget_preference', 'Not provided')}
- Learning Style: {user_data.get('learning_style', 'Not provided')}
- Personality Type: {user_data.get('personality_type', 'Not provided')}
- Additional Info: {user_data.get('additional_info', 'Not provided')}

{f"RESUME HIGHLIGHTS: {user_data.get('resume_content', '')[:1000]}" if 'resume_content' in user_data else ''}

---

🎯 **TASK:**  
Create a detailed and visually organized **career roadmap** for the user in **{user_data.get('mode', 'detailed')} mode**.
Follow this format and ensure all outputs are in **structured bullet points with subpoints**.

---

## 1. POSSIBLE CAREER PATHS
List 3-4 suitable career tracks based on their skills and interests (e.g., "AI Engineer", "Data Scientist", "Full Stack Developer"),  
each with:
• Overview of role
  → What the role involves
  → Day-to-day responsibilities
• Required core skills
  → Technical skills needed
  → Soft skills needed
• Pros & cons
  → Advantages of this path
  → Challenges to consider
• Typical starting positions
  → Entry-level roles
  → Junior positions
• Expected timeline to job-readiness
  → With their current profile
  → Estimated months/years

---

## 2. SELECTED CAREER TRACK: {user_data.get('desired_role', "User's preferred role")}
Provide a **customized roadmap** based on their current profile and chosen direction.

### a. Immediate Action Items (Next 1–3 Months)
• Quick wins and foundational improvements
  → Specific daily/weekly actions
  → Priority skills to start with
• Resources or short courses to begin with
  → Course names with platforms and URLs
  → Free resources available
• Resume and LinkedIn improvements
  → Specific sections to enhance
  → Keywords to add
  → Profile optimization tips

### b. Short-Term Goals (3–6 Months)
• Skill-building plan
  → Core technologies to master
  → Practice platforms (LeetCode, HackerRank, etc.)
  → Time allocation per skill
• Real-world projects to build
  → 2-3 beginner to intermediate projects
  → Technologies to use
  → Where to host/showcase
• Certifications to pursue (free or paid based on budget)
  → Certification names
  → Platforms
  → Expected time commitment
  → Value in job market
• Networking & community goals
  → Communities to join (Reddit, Discord, LinkedIn groups)
  → Events or webinars to attend
  → How to contribute

### c. Medium-Term Goals (6–12 Months)
• Advanced skill development
  → Specialized technologies
  → Advanced concepts to master
  → System design and architecture
• Advanced project ideas
  → 2-3 intermediate to advanced projects
  → Real-world problem solving
  → Technologies and best practices
• Internship or freelance guidance
  → Where to find opportunities
  → How to apply effectively
  → Portfolio presentation
• Interview preparation roadmap
  → DSA preparation strategy
  → System design practice
  → Behavioral interview prep
  → Mock interview platforms

### d. Long-Term Career Path (1–3 Years)
• Specialization focus
  → Areas to deep-dive
  → Industry certifications
  → Emerging technologies to watch
• Transition opportunities
  → Career progression paths
  → Salary expectations at each level
  → Geographic opportunities
• Leadership and growth roadmap
  → Soft skills development
  → Mentorship opportunities
  → Contributing to open source
  → Building personal brand

---

## 3. SKILLS GAP ANALYSIS
• Current Skills Assessment
  → Skills they already have
  → Proficiency levels
• Required Industry Skills
  → Must-have skills for desired role
  → Nice-to-have skills
  → Emerging skills in the industry
• Priority Learning Order
  → Skill 1 (Why first, estimated time)
  → Skill 2 (Why next, estimated time)
  → Skill 3 (Why after, estimated time)
• Estimated Timeline
  → Time to become job-ready
  → Milestones to track progress

---

## 4. PROJECT IDEAS (Practical Portfolio Builders)
For each project (3–5 projects):
• Project Name
  → Brief description
  → Problem it solves
• Tech Stack
  → Frontend technologies
  → Backend technologies
  → Database and tools
• Learning Outcomes
  → Skills demonstrated
  → Complexity level
• Implementation Tips
  → Where to start
  → Resources to use
  → Time estimate
• Showcase Strategy
  → GitHub repository structure
  → Live demo hosting
  → README documentation

---

## 5. COURSES & RESOURCES
For each key skill area, recommend:
• Course Title
  → Full name of course
• Platform & URL
  → Coursera, Udemy, edX, freeCodeCamp, etc.
  → Direct link if possible
• Duration & Effort
  → Hours per week
  → Total weeks/months
• Why It's Relevant
  → How it aligns with career goals
  → Skills covered
• Cost Indicator
  → Free / Paid / Free with certificate option
  → Fits their budget preference: {user_data.get('budget_preference', 'Affordable')}
• Learning Path Integration
  → When to take this course
  → Prerequisites if any

Include resources matching their learning style: {user_data.get('learning_style', 'Mixed')}

---

## 6. NETWORKING & PERSONAL BRANDING
• Online Communities to Join
  → Platform-specific communities
  → Why each community is valuable
  → How to actively participate
• LinkedIn Strategy
  → Profile optimization checklist
  → Content posting strategy
  → Connection building approach
  → Engagement tips
• GitHub Strategy
  → Repository organization
  → Contributing to open source
  → Building visibility
  → README best practices
• Conferences, Hackathons & Events
  → Relevant events to attend
  → How to prepare
  → Networking strategies
• Personal Brand Building
  → Blog or portfolio website
  → Social media presence
  → Building thought leadership

---

## 7. JOB SEARCH STRATEGY
• Resume Optimization
  → ATS-friendly formatting
  → Key sections to highlight
  → Action verbs to use
  → Quantifying achievements
• Company Targeting Strategy
  → Startups vs Product companies vs MNCs
  → Based on preference: {user_data.get('preferred_work_type', 'Flexible')}
  → Research approach
• Job Search Platforms
  → LinkedIn, Indeed, AngelList, etc.
  → Company career pages
  → Referral strategies
• Application Strategy
  → Number of applications per week
  → Customization approach
  → Follow-up tactics
• Interview Preparation
  → Technical interview prep timeline
  → Behavioral questions practice
  → Mock interview platforms
  → Salary negotiation tips

---

## 8. ADDITIONAL RECOMMENDATIONS
• Books to Read
  → Technical books
  → Career development books
  → Industry-specific reads
• YouTube Channels to Follow
  → Channel names with focus areas
  → Why each channel is valuable
• Podcasts for Learning & Inspiration
  → Podcast names
  → Key topics covered
• Thought Leaders & Mentors
  → Industry experts to follow
  → Where to find them (Twitter, LinkedIn, etc.)
• Learning Resources
  → Documentation sites
  → Tutorial platforms
  → Practice platforms

---

## 9. TIMELINE & MILESTONES
Create a visual timeline for {user_data.get('roadmap_duration', '1 year')} with:
• Month-by-month breakdown
  → What to focus on each month
  → Key milestones
  → Deliverables
• Progress Tracking Metrics
  → How to measure progress
  → KPIs for success
• Adjustment Points
  → When to reassess
  → How to pivot if needed

---

## 10. MOTIVATION & MINDSET
• Realistic Expectations
  → What to expect in this journey
  → Common challenges
• Staying Motivated
  → Tips for consistency
  → Handling setbacks
• Work-Life Balance
  → Given {user_data.get('available_hours_per_week', '10-15')} hours/week
  → Avoiding burnout
• Success Stories
  → Similar profiles who succeeded
  → Inspiration and proof of concept

---

**Output Format Rules:**
- Use clear bullet points (•) with nested subpoints (→ or —)
- Keep tone motivational yet realistic
- Organize each section with headers (##) and subheaders (###)
- Align recommendations with:
  * Available time: {user_data.get('available_hours_per_week', '10-15')} hours/week
  * Roadmap duration: {user_data.get('roadmap_duration', '1 year')}
  * Budget: {user_data.get('budget_preference', 'Affordable')}
  * Learning style: {user_data.get('learning_style', 'Mixed')}
  * Personality: {user_data.get('personality_type', 'Balanced')}
- Provide specific, actionable advice with URLs where possible
- Format in {user_data.get('mode', 'detailed')} mode

Generate the roadmap now.
"""
        
        print("\n🤖 Generating personalized career roadmap...")
        print("⏳ This may take a moment...\n")
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating career path: {e}"
    
    def save_roadmap(self, roadmap, user_data):
        """Save the generated roadmap to a file"""
        filename = f"career_roadmap_{user_data.get('desired_role', 'user').replace(' ', '_').replace('/', '_')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("PERSONALIZED CAREER ROADMAP\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated for: {user_data.get('college', 'N/A')}\n")
            f.write(f"Desired Role: {user_data.get('desired_role', 'N/A')}\n")
            f.write(f"Branch: {user_data.get('branch', 'N/A')}\n")
            f.write(f"Duration: {user_data.get('roadmap_duration', 'N/A')}\n")
            f.write(f"Mode: {user_data.get('mode', 'detailed').title()}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(roadmap)
        
        return filename
    
    def run(self):
        """Main execution flow"""
        try:
            # Collect user information
            user_data = self.collect_user_info()
            
            # Generate career path
            roadmap = self.generate_career_path(user_data)
            
            # Display roadmap
            print("\n" + "="*80)
            print("YOUR PERSONALIZED CAREER ROADMAP")
            print("="*80 + "\n")
            print(roadmap)
            
            # Save to file
            filename = self.save_roadmap(roadmap, user_data)
            print(f"\n✅ Career roadmap saved to: {filename}")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Process interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def run_with_data(self, user_data):
        """Run the planner with pre-filled data (for testing)"""
        try:
            # Generate career path
            roadmap = self.generate_career_path(user_data)
            
            # Display roadmap
            print("\n" + "="*80)
            print("YOUR PERSONALIZED CAREER ROADMAP")
            print("="*80 + "\n")
            print(roadmap)
            
            # Save to file
            filename = self.save_roadmap(roadmap, user_data)
            print(f"\n✅ Career roadmap saved to: {filename}")
            
            return roadmap, filename
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None, None


def test_with_sample_data():
    
    
    print("\n" + "="*80)
    print("TESTING CAREER PATH PLANNER WITH SAMPLE DATA".center(80))
    print("="*80 + "\n")
    
    # Comprehensive sample test data with all new fields
    test_data = {
        'college': 'IIT Delhi',
        'branch': 'Computer Science Engineering',
        'cgpa': '8.5',
        'skills': 'Python, JavaScript, React, Node.js, SQL, Git, Docker',
        'interests': 'Web Development, Machine Learning, Cloud Computing, System Design',
        'strengths': 'Problem-solving, Quick learner, Team collaboration, Analytical thinking',
        'weaknesses': 'Public speaking, Time management under pressure',
        'certifications_done': 'AWS Cloud Practitioner, Python for Data Science',
        'projects': 'E-commerce website (MERN stack), ML Chatbot (NLP), Real-time Analytics Dashboard',
        'internship_experience': '2 internships - 1 at startup (6 months), 1 at mid-size tech company (3 months)',
        'desired_role': 'Full Stack Developer',
        'target_industry': 'Product-based companies, Tech startups',
        'preferred_work_type': 'Hybrid',
        'available_hours_per_week': '15-20',
        'roadmap_duration': '1 year',
        'learning_style': 'Mixed',
        'personality_type': 'Analytical',
        'budget_preference': 'Affordable (<$50/month)',
        'mode': 'detailed',
        'additional_info': 'Active on GitHub, contributed to 2 open-source projects, looking for opportunities in product-based companies'
    }
    
    print("📋 Comprehensive Test Data:")
    print("-" * 80)
    for key, value in test_data.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("-" * 80)
    
    proceed = input("\n➡️  Proceed with this test data? (y/n): ").strip().lower()
    
    if proceed == 'y':
        planner = CareerPathPlanner()
        roadmap, filename = planner.run_with_data(test_data)
        
        if roadmap:
            print("\n✅ Test completed successfully!")
            print(f"📄 Results saved to: {filename}")
    else:
        print("\n❌ Test cancelled")


def test_interactive_mode():
    # Run in normal interactive mode with all new fields

    print("\n" + "="*80)
    print("INTERACTIVE MODE - ENTER YOUR DATA".center(80))
    print("="*80 + "\n")
    
    planner = CareerPathPlanner()
    planner.run()


def test_custom_data():
    # Test with custom data that user provides - simplified version
        
    print("\n" + "="*80)
    print("QUICK CUSTOM TEST MODE".center(80))
    print("="*80 + "\n")
    
    user_data = {}
    
    print("Enter basic test data (press Enter to use defaults):\n")
    
    user_data['college'] = input("College: ").strip() or "Test University"
    user_data['branch'] = input("Branch: ").strip() or "CSE"
    user_data['cgpa'] = input("CGPA: ").strip() or "8.0"
    user_data['skills'] = input("Skills: ").strip() or "Python, Java, JavaScript"
    user_data['interests'] = input("Interests: ").strip() or "Software Development, AI"
    user_data['strengths'] = input("Strengths: ").strip() or "Problem-solving, Coding"
    user_data['weaknesses'] = input("Weaknesses: ").strip() or "Public speaking"
    user_data['certifications_done'] = input("Certifications: ").strip() or "None"
    user_data['projects'] = input("Projects: ").strip() or "Portfolio website, Todo app"
    user_data['internship_experience'] = input("Internships: ").strip() or "1 internship (3 months)"
    user_data['desired_role'] = input("Desired Role: ").strip() or "Software Engineer"
    user_data['target_industry'] = input("Target Industry: ").strip() or "Tech"
    user_data['preferred_work_type'] = input("Work Type (Remote/On-site/Hybrid): ").strip() or "Hybrid"
    user_data['available_hours_per_week'] = input("Hours/week for learning: ").strip() or "10-15"
    user_data['roadmap_duration'] = input("Duration (6 months/1 year/2-3 years): ").strip() or "1 year"
    user_data['learning_style'] = input("Learning Style: ").strip() or "Mixed"
    user_data['personality_type'] = input("Personality: ").strip() or "Analytical"
    user_data['budget_preference'] = input("Budget (Free Only/Affordable/Premium): ").strip() or "Affordable"
    user_data['mode'] = input("Mode (short/detailed/executive summary): ").strip() or "detailed"
    user_data['additional_info'] = input("Additional Info: ").strip() or ""
    
    print("\n" + "-"*80)
    print("Test data entered - generating roadmap...")
    print("-"*80)
    
    planner = CareerPathPlanner()
    planner.run_with_data(user_data)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ADVANCED CAREER PATH PLANNER - TEST SUITE".center(80))
    print("="*80 + "\n")
    
    print("Choose a test mode:")
    print("1. Test with comprehensive sample data (automated)")
    print("2. Test with custom data (quick entry)")
    print("3. Interactive mode (full manual entry with all fields)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        test_with_sample_data()
    elif choice == '2':
        test_custom_data()
    elif choice == '3':
        test_interactive_mode()
    elif choice == '4':
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice. Please run again and select 1-4.")