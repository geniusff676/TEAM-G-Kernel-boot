#!/usr/bin/env python3
"""
test_api.py - Test client for the unified Career Development API
Demonstrates how to use all three services
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:5000"
SESSION_ID = "test-session-123"

class CareerAPIClient:
    """Client for interacting with the unified Career Development API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session_id = SESSION_ID
    
    # ============================================
    # General Endpoints
    # ============================================
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health and service availability"""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get API documentation and endpoints"""
        response = requests.get(f"{self.base_url}/")
        return response.json()
    
    # ============================================
    # Roadmap Service
    # ============================================
    
    def generate_roadmap(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate career roadmap"""
        response = requests.post(
            f"{self.base_url}/api/roadmap/generate",
            json=user_data
        )
        return response.json()
    
    def upload_resume(self, file_path: str) -> Dict[str, Any]:
        """Upload and process resume PDF"""
        with open(file_path, 'rb') as f:
            files = {'resume': f}
            response = requests.post(
                f"{self.base_url}/api/roadmap/upload-resume",
                files=files
            )
        return response.json()
    
    def generate_roadmap_with_resume(self, file_path: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate roadmap with resume upload"""
        with open(file_path, 'rb') as f:
            files = {'resume': f}
            data = {'data': json.dumps(user_data)}
            response = requests.post(
                f"{self.base_url}/api/roadmap/generate-with-resume",
                files=files,
                data=data
            )
        return response.json()
    
    # ============================================
    # Chat Service
    # ============================================
    
    def ask_chat(self, query: str, include_history: bool = True) -> Dict[str, Any]:
        """Ask career counselor a question"""
        response = requests.post(
            f"{self.base_url}/api/chat/ask",
            json={
                "session_id": self.session_id,
                "query": query,
                "include_history": include_history
            }
        )
        return response.json()
    
    def update_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        response = requests.post(
            f"{self.base_url}/api/chat/profile",
            json={
                "session_id": self.session_id,
                "profile": profile_data
            }
        )
        return response.json()
    
    def get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        response = requests.get(
            f"{self.base_url}/api/chat/profile",
            params={"session_id": self.session_id}
        )
        return response.json()
    
    def get_history(self, limit: int = None) -> Dict[str, Any]:
        """Get conversation history"""
        params = {"session_id": self.session_id}
        if limit:
            params["limit"] = limit
        response = requests.get(
            f"{self.base_url}/api/chat/history",
            params=params
        )
        return response.json()
    
    def clear_history(self) -> Dict[str, Any]:
        """Clear conversation history"""
        response = requests.delete(
            f"{self.base_url}/api/chat/history",
            json={"session_id": self.session_id}
        )
        return response.json()
    
    def get_advice(self, topic: str) -> Dict[str, Any]:
        """Get specific career advice"""
        response = requests.get(
            f"{self.base_url}/api/chat/advice/{topic}",
            params={"session_id": self.session_id}
        )
        return response.json()
    
    # ============================================
    # Course Recommender Service
    # ============================================
    
    def recommend_courses(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Get course recommendations"""
        response = requests.post(
            f"{self.base_url}/api/courses/recommend",
            json={
                "query": query,
                "top_k": top_k
            }
        )
        return response.json()


# ============================================
# Example Usage
# ============================================

def print_section(title: str):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def main():
    """Run example tests for all services"""
    
    print("\n🎓 Career Development API - Test Client")
    print("="*60)
    
    # Initialize client
    client = CareerAPIClient()
    
    # 1. Check API Health
    print_section("1. API Health Check")
    try:
        health = client.health_check()
        print(json.dumps(health, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Test Roadmap Service
    print_section("2. Generate Career Roadmap")
    try:
        roadmap_data = {
            "desired_role": "Full Stack Developer",
            "branch": "Computer Science",
            "skills": "JavaScript, React, Node.js",
            "cgpa": "8.0",
            "roadmap_duration": "6 months",
            "budget_preference": "Affordable",
            "available_hours_per_week": "15-20"
        }
        
        result = client.generate_roadmap(roadmap_data)
        
        if result['status'] == 'success':
            print("✅ Roadmap generated successfully!")
            print(f"Duration: {result['data']['user_profile']['duration']}")
            print(f"Role: {result['data']['user_profile']['desired_role']}")
            
            # Print first few lines of roadmap
            roadmap_text = result['data']['roadmap_text']
            print("\nRoadmap Preview:")
            print(roadmap_text[:500] + "...\n")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Test Chat Service
    print_section("3. Career Counselor Chat")
    try:
        # Update profile first
        profile = {
            "education": "Bachelor's in Computer Science",
            "experience": "1 year internship",
            "skills": ["Python", "JavaScript", "React"],
            "interests": ["Web Development", "AI"],
            "goals": "Become a senior full-stack developer"
        }
        
        profile_result = client.update_profile(profile)
        print("✅ Profile updated")
        
        # Ask a question
        question = "What are the most important skills I should focus on for full-stack development?"
        chat_result = client.ask_chat(question)
        
        if chat_result['status'] == 'success':
            print(f"\n💬 Question: {question}")
            print(f"\n🤖 Answer: {chat_result['data']['response'][:300]}...\n")
        else:
            print(f"❌ Error: {chat_result['message']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Test Course Recommender
    print_section("4. Course Recommendations")
    try:
        query = "full stack web development javascript react node"
        courses = client.recommend_courses(query, top_k=3)
        
        if courses['status'] == 'success':
            print(f"Query: {query}\n")
            print(f"Found {courses['data']['total_recommendations']} recommendations:\n")
            
            for i, course in enumerate(courses['data']['top_courses'], 1):
                print(f"{i}. {course['course_title']}")
                print(f"   Organization: {course['organization']}")
                print(f"   Similarity: {course['similarity_score']:.3f}")
                print(f"   URL: {course['url']}")
                print()
        else:
            print(f"❌ Error: {courses['message']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Get Career Advice
    print_section("5. Get Specific Career Advice")
    try:
        advice = client.get_advice("interview")
        
        if advice['status'] == 'success':
            print(f"Topic: {advice['data']['topic']}")
            print(f"\nAdvice: {advice['data']['response'][:300]}...\n")
        else:
            print(f"❌ Error: {advice['message']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test client stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")