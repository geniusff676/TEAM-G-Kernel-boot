#!/usr/bin/env python3
"""
career_assistant.py - AI Career Counselor using Google GenAI SDK (gemini-2.5-flash)
Modular design for easy integration with Flask or other applications.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Try to import the GenAI SDK
try:
    from google import genai
    from google.genai import types
    GEMINI_SDK_AVAILABLE = True
except Exception:
    GEMINI_SDK_AVAILABLE = False
    genai = None
    types = None

# Data storage
DATA_DIR = os.path.join(os.path.expanduser("~"), ".career_counselor")
os.makedirs(DATA_DIR, exist_ok=True)
CONVERSATION_HISTORY_FILE = os.path.join(DATA_DIR, "conversations.json")
USER_PROFILES_FILE = os.path.join(DATA_DIR, "user_profiles.json")

# -----------------------------
# JSON persistence helpers
# -----------------------------
def load_json(path: str, default: Any) -> Any:
    """Load JSON data from file with error handling"""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"Error loading JSON from {path}: {e}")
        return default

def save_json(path: str, data: Any) -> bool:
    """Save JSON data to file with error handling"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON to {path}: {e}")
        return False

# -----------------------------
# Enhanced Gemini Client for Career Counseling
# -----------------------------
class GeminiCareerClient:
    """
    Wrapper around google.genai.Client optimized for career counseling
    with Gemini 2.5 Flash model.
    """
    def __init__(self, model: str = "gemini-2.5-flash"):
        if not GEMINI_SDK_AVAILABLE:
            raise RuntimeError(
                "GenAI SDK not installed. Install it with: pip install google-genai"
            )
        
        self.model = model
        
        try:
            if GEMINI_KEY:
                self.client = genai.Client(api_key=GEMINI_KEY)
            else:
                raise RuntimeError("GEMINI_API_KEY not found in environment")
                
            # Test the connection
            self._test_connection()
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize genai.Client(): {str(e)}")

    def _test_connection(self) -> None:
        """Test if the Gemini connection is working"""
        try:
            test_contents = [types.UserContent(parts=[types.Part.from_text(text="Hello")])]
            config = types.GenerateContentConfig(
                max_output_tokens=10,
                temperature=0.1
            )
            self.client.models.generate_content(
                model=self.model,
                contents=test_contents,
                config=config
            )
        except Exception as e:
            raise RuntimeError(f"Gemini API test failed: {str(e)}")

    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_instruction: str = "",
        max_output_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a response from Gemini with enhanced error handling
        """
        try:
            contents = []
            
            # Process messages
            for m in messages:
                role = m.get("role", "user")
                text = str(m.get("content", "") or m.get("text", ""))
                
                if not text.strip():
                    continue
                    
                if role == "assistant" or role == "model":
                    contents.append(types.ModelContent(parts=[types.Part.from_text(text=text)]))
                elif role == "system":
                    if not system_instruction:
                        system_instruction = text
                else:  # user or any other role
                    contents.append(types.UserContent(parts=[types.Part.from_text(text=text)]))

            # Ensure at least one user content exists
            if not contents:
                contents = [types.UserContent(parts=[types.Part.from_text(text="Hello")])]

            # Configuration for high-quality responses
            config = types.GenerateContentConfig(
                system_instruction=system_instruction if system_instruction else None,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=0.95,
                top_k=40,
            )

            # Generate content
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config
            )
            
            # Extract response text
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            
            # Fallback extraction
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        return candidate.content.parts[0].text.strip()
            
            return "I apologize, but I couldn't generate a proper response. Please try again."
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return "I've reached my usage limits. Please try again in a few minutes."
            elif "api" in error_msg.lower() and "key" in error_msg.lower():
                return "There's an issue with the API configuration. Please check your GEMINI_API_KEY."
            else:
                return f"I encountered an error: {error_msg}"

# -----------------------------
# Career Counselor Assistant
# -----------------------------
class CareerCounselor:
    """
    AI Career Counselor that provides guidance on career choices, skills development,
    job search, and professional growth.
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize the Career Counselor
        
        Args:
            session_id: Optional session identifier for conversation tracking
        """
        self.session_id = session_id or f"session_{int(time.time() * 1000)}"
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_profile: Dict[str, Any] = {}
        self.gemini_client: Optional[GeminiCareerClient] = None
        
        # Load existing data
        self._load_conversation_history()
        self._load_user_profile()
        
        # Initialize Gemini client
        if GEMINI_SDK_AVAILABLE:
            try:
                self.gemini_client = GeminiCareerClient()
                print("✅ Gemini 2.5 Flash initialized for career counseling")
            except Exception as e:
                print(f"⚠️ Warning: Gemini client initialization failed: {e}")
                self.gemini_client = None
        else:
            print("⚠️ Warning: google-genai SDK not installed")
            
        # Career counseling system prompt
        self.system_prompt = """You are an expert AI Career Counselor with deep knowledge in:

**YOUR EXPERTISE:**
- Career guidance and path planning
- Skills assessment and development
- Resume and interview preparation
- Job search strategies
- Industry trends and insights
- Work-life balance and professional growth
- Educational pathways and certifications
- Salary negotiation and career advancement
- Career transition and pivot strategies
- Freelancing and entrepreneurship guidance

**YOUR APPROACH:**
1. **Empathetic & Supportive**: Understand the user's situation, concerns, and aspirations
2. **Personalized**: Tailor advice based on their background, skills, and goals
3. **Actionable**: Provide specific, practical steps they can take immediately
4. **Comprehensive**: Consider multiple angles and options
5. **Realistic**: Balance optimism with practical considerations
6. **Current**: Stay aware of modern job market trends and requirements

**YOUR COMMUNICATION STYLE:**
- Warm, encouraging, and professional
- Use clear, accessible language
- Break down complex topics into digestible parts
- Provide examples and real-world scenarios
- Ask clarifying questions when needed
- Celebrate their strengths and progress
- Address concerns honestly and constructively

**KEY TOPICS YOU HELP WITH:**
- Choosing a career path or major
- Skill gap analysis and learning roadmaps
- Resume/CV optimization and LinkedIn profiles
- Interview preparation and common questions
- Job search strategies and networking
- Salary negotiation techniques
- Career change and transition planning
- Professional development and upskilling
- Work culture and company evaluation
- Freelancing, consulting, and entrepreneurship
- Industry-specific advice (tech, finance, healthcare, etc.)
- Educational opportunities and certifications

**IMPORTANT GUIDELINES:**
- Never guarantee job outcomes or specific salaries
- Acknowledge when you need more information about the user
- Encourage continuous learning and adaptability
- Emphasize soft skills alongside technical skills
- Consider the user's life circumstances and constraints
- Promote ethical career practices
- Suggest multiple options when relevant

**CURRENT CONTEXT:**
- Date: {current_date}
- You maintain conversation context to provide personalized guidance
- You remember user's background when they share it
- You can help with career planning at any stage (student, professional, career changer)

Remember: You're here to empower users to make informed career decisions and achieve their professional goals. Be their trusted advisor and advocate."""

    def _load_conversation_history(self) -> None:
        """Load conversation history for this session"""
        all_conversations = load_json(CONVERSATION_HISTORY_FILE, {})
        self.conversation_history = all_conversations.get(self.session_id, [])

    def _save_conversation_history(self) -> None:
        """Save conversation history for this session"""
        all_conversations = load_json(CONVERSATION_HISTORY_FILE, {})
        all_conversations[self.session_id] = self.conversation_history
        save_json(CONVERSATION_HISTORY_FILE, all_conversations)

    def _load_user_profile(self) -> None:
        """Load user profile for this session"""
        all_profiles = load_json(USER_PROFILES_FILE, {})
        self.user_profile = all_profiles.get(self.session_id, {})

    def _save_user_profile(self) -> None:
        """Save user profile for this session"""
        all_profiles = load_json(USER_PROFILES_FILE, {})
        all_profiles[self.session_id] = self.user_profile
        save_json(USER_PROFILES_FILE, all_profiles)

    def _get_context_enhanced_prompt(self) -> str:
        """Generate system prompt with user context"""
        current_date = datetime.now().strftime("%B %d, %Y")
        base_prompt = self.system_prompt.format(current_date=current_date)
        
        # Add user profile context if available
        if self.user_profile:
            context_parts = []
            if self.user_profile.get("education"):
                context_parts.append(f"Education: {self.user_profile['education']}")
            if self.user_profile.get("experience"):
                context_parts.append(f"Experience: {self.user_profile['experience']}")
            if self.user_profile.get("skills"):
                context_parts.append(f"Skills: {', '.join(self.user_profile['skills'])}")
            if self.user_profile.get("interests"):
                context_parts.append(f"Career Interests: {', '.join(self.user_profile['interests'])}")
            if self.user_profile.get("goals"):
                context_parts.append(f"Goals: {self.user_profile['goals']}")
                
            if context_parts:
                base_prompt += "\n\n**USER PROFILE:**\n" + "\n".join(context_parts)
        
        return base_prompt

    def update_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Update user profile information
        
        Args:
            profile_data: Dictionary containing profile fields
            
        Returns:
            Status dictionary
        """
        try:
            self.user_profile.update(profile_data)
            self.user_profile["last_updated"] = datetime.now().isoformat()
            self._save_user_profile()
            
            return {
                "status": "success",
                "message": "Profile updated successfully",
                "profile": self.user_profile
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update profile: {str(e)}"
            }

    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        return self.user_profile.copy()

    def ask(
        self, 
        query: str, 
        include_history: bool = True,
        max_history: int = 10
    ) -> Dict[str, Any]:
        """
        Get career counseling advice
        
        Args:
            query: User's question or request
            include_history: Whether to include conversation history
            max_history: Maximum number of previous exchanges to include
            
        Returns:
            Dictionary with response and metadata
        """
        if not self.gemini_client:
            return {
                "status": "error",
                "response": "Career counselor is not available. Please check your GEMINI_API_KEY configuration.",
                "session_id": self.session_id
            }

        try:
            # Build messages with history
            messages = []
            
            if include_history and self.conversation_history:
                # Include recent history (limit to max_history exchanges)
                recent_history = self.conversation_history[-(max_history * 2):]
                for entry in recent_history:
                    messages.append({
                        "role": entry["role"],
                        "content": entry["content"]
                    })
            
            # Add current query
            messages.append({
                "role": "user",
                "content": query
            })
            
            # Get enhanced system prompt with user context
            system_prompt = self._get_context_enhanced_prompt()
            
            # Generate response
            response = self.gemini_client.generate_response(
                messages=messages,
                system_instruction=system_prompt,
                max_output_tokens=2048,
                temperature=0.7
            )
            
            # Save to history
            timestamp = datetime.now().isoformat()
            self.conversation_history.append({
                "role": "user",
                "content": query,
                "timestamp": timestamp
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": timestamp
            })
            
            # Keep history manageable (last 100 messages)
            if len(self.conversation_history) > 100:
                self.conversation_history = self.conversation_history[-100:]
            
            self._save_conversation_history()
            
            return {
                "status": "success",
                "response": response,
                "session_id": self.session_id,
                "timestamp": timestamp
            }
            
        except Exception as e:
            return {
                "status": "error",
                "response": f"Error generating response: {str(e)}",
                "session_id": self.session_id
            }

    def get_conversation_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history for this session
        
        Args:
            limit: Optional limit on number of messages to return
            
        Returns:
            List of conversation messages
        """
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history.copy()

    def clear_history(self) -> Dict[str, str]:
        """Clear conversation history for this session"""
        try:
            self.conversation_history = []
            self._save_conversation_history()
            return {
                "status": "success",
                "message": "Conversation history cleared"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to clear history: {str(e)}"
            }

    def get_career_advice(self, topic: str) -> Dict[str, Any]:
        """
        Get specific career advice on a topic
        
        Args:
            topic: Career topic (e.g., 'resume', 'interview', 'skills')
            
        Returns:
            Response dictionary
        """
        topic_prompts = {
            "resume": "I need help creating or improving my resume. Can you provide comprehensive guidance on resume best practices, formatting, and what to include?",
            "interview": "I have a job interview coming up. Can you help me prepare with common interview questions and tips?",
            "skills": "What are the most in-demand skills in the current job market? How can I develop them?",
            "career_change": "I'm considering changing my career. What steps should I take to make a successful transition?",
            "salary": "How should I approach salary negotiation? What research should I do beforehand?",
            "networking": "How can I effectively network to advance my career?",
            "linkedin": "How can I optimize my LinkedIn profile to attract recruiters and opportunities?",
            "job_search": "What are the most effective strategies for finding and landing a new job?",
            "upskilling": "What skills should I focus on learning to stay competitive in my field?",
            "work_life_balance": "How can I maintain a healthy work-life balance while advancing my career?"
        }
        
        prompt = topic_prompts.get(
            topic.lower(),
            f"Can you provide comprehensive guidance on {topic} in a career context?"
        )
        
        return self.ask(prompt, include_history=False)

# -----------------------------
# Utility functions for easy use
# -----------------------------
def create_counselor(session_id: Optional[str] = None) -> CareerCounselor:
    """
    Factory function to create a CareerCounselor instance
    
    Args:
        session_id: Optional session identifier
        
    Returns:
        CareerCounselor instance
    """
    return CareerCounselor(session_id=session_id)

def quick_advice(query: str) -> str:
    """
    Quick function to get career advice without session management
    
    Args:
        query: Career question
        
    Returns:
        Response text
    """
    counselor = CareerCounselor()
    result = counselor.ask(query, include_history=False)
    return result.get("response", "Unable to generate response")

# -----------------------------
# CLI Interface (optional)
# -----------------------------
def main():
    """Command-line interface for career counselor"""
    print("🎓 AI Career Counselor")
    print("=" * 60)
    print("Powered by Gemini 2.5 Flash")
    print()
    
    if not GEMINI_KEY:
        print("❌ Error: GEMINI_API_KEY not found in environment")
        print("Please set your API key in .env file or environment variables")
        print("Get your key from: https://aistudio.google.com/app/apikey")
        return
    
    if not GEMINI_SDK_AVAILABLE:
        print("❌ Error: google-genai SDK not installed")
        print("Install with: pip install google-genai")
        return
    
    # Create counselor instance
    counselor = CareerCounselor()
    
    print("👋 Hello! I'm your AI Career Counselor.")
    print("I can help you with:")
    print("  • Career planning and advice")
    print("  • Resume and interview preparation")
    print("  • Skill development guidance")
    print("  • Job search strategies")
    print("  • And much more!")
    print()
    print("Commands:")
    print("  /profile - Set your profile information")
    print("  /history - View conversation history")
    print("  /clear - Clear conversation history")
    print("  /quit - Exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n👋 Good luck with your career journey! Feel free to return anytime.")
                break
            
            if user_input.lower() == '/history':
                history = counselor.get_conversation_history(limit=10)
                if history:
                    print("\n📜 Recent conversation:")
                    for msg in history[-10:]:
                        role = "You" if msg["role"] == "user" else "Counselor"
                        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                        print(f"  {role}: {content}")
                    print()
                else:
                    print("\n📜 No conversation history yet.\n")
                continue
            
            if user_input.lower() == '/clear':
                counselor.clear_history()
                print("\n✅ Conversation history cleared.\n")
                continue
            
            if user_input.lower() == '/profile':
                print("\n📝 Let's update your profile (press Enter to skip any field):")
                education = input("  Education: ").strip()
                experience = input("  Years of experience: ").strip()
                skills = input("  Key skills (comma-separated): ").strip()
                interests = input("  Career interests (comma-separated): ").strip()
                goals = input("  Career goals: ").strip()
                
                profile_data = {}
                if education:
                    profile_data["education"] = education
                if experience:
                    profile_data["experience"] = experience
                if skills:
                    profile_data["skills"] = [s.strip() for s in skills.split(",")]
                if interests:
                    profile_data["interests"] = [i.strip() for i in interests.split(",")]
                if goals:
                    profile_data["goals"] = goals
                
                if profile_data:
                    result = counselor.update_user_profile(profile_data)
                    print(f"\n✅ {result['message']}\n")
                else:
                    print("\n⚠️ No profile data updated.\n")
                continue
            
            # Get career advice
            print("\nCounselor: ", end="", flush=True)
            result = counselor.ask(user_input)
            
            if result["status"] == "success":
                print(result["response"])
            else:
                print(f"❌ {result['response']}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Good luck with your career journey!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()