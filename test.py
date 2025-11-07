# from career_assistant import CareerCounselor

# counselor = CareerCounselor(session_id="user_123")
# result = counselor.ask("What skills should I learn as a developer?")
# print(result['response'])#!/usr/bin/env python3
"""
test_client.py - Test client for AI Career Counselor API
Demonstrates how to interact with the Flask API endpoints.
"""

import requests
import json
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:5000/api"
SESSION_ID = "test_session_123"

def print_response(response: requests.Response, title: str = "Response"):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print(f"{'='*60}\n")

def test_health_check():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print_response(response, "Health Check")
    return response.status_code == 200

def test_get_topics():
    """Test getting available topics"""
    print("\n📚 Testing Get Topics...")
    response = requests.get(f"{API_BASE_URL}/topics")
    print_response(response, "Available Topics")
    return response.status_code == 200

def test_chat(query: str, session_id: str = SESSION_ID):
    """Test chat endpoint"""
    print(f"\n💬 Testing Chat with query: '{query}'...")
    
    payload = {
        "session_id": session_id,
        "query": query,
        "include_history": True
    }
    
    response = requests.post(f"{API_BASE_URL}/chat", json=payload)
    print_response(response, f"Chat Response for: '{query}'")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            print(f"✅ Career Counselor Response:")
            print(f"{data['data']['response'][:500]}...")
            return True
    
    return False

def test_update_profile(session_id: str = SESSION_ID):
    """Test profile update endpoint"""
    print("\n👤 Testing Profile Update...")
    
    payload = {
        "session_id": session_id,
        "profile": {
            "education": "Bachelor's in Computer Science",
            "experience": "2 years",
            "skills": ["Python", "JavaScript", "React", "Machine Learning"],
            "interests": ["Software Development", "AI/ML", "Web Development"],
            "goals": "Become a senior software engineer specializing in AI"
        }
    }
    
    response = requests.post(f"{API_BASE_URL}/profile", json=payload)
    print_response(response, "Profile Update")
    return response.status_code == 200

def test_get_profile(session_id: str = SESSION_ID):
    """Test getting profile"""
    print("\n👤 Testing Get Profile...")
    
    response = requests.get(f"{API_BASE_URL}/profile", params={"session_id": session_id})
    print_response(response, "Get Profile")
    return response.status_code == 200

def test_get_history(session_id: str = SESSION_ID, limit: int = 5):
    """Test getting conversation history"""
    print("\n📜 Testing Get History...")
    
    params = {
        "session_id": session_id,
        "limit": limit
    }
    
    response = requests.get(f"{API_BASE_URL}/history", params=params)
    print_response(response, f"Conversation History (last {limit} messages)")
    return response.status_code == 200

def test_get_advice(topic: str):
    """Test getting specific career advice"""
    print(f"\n💡 Testing Get Advice for topic: '{topic}'...")
    
    response = requests.get(f"{API_BASE_URL}/advice/{topic}", params={"session_id": SESSION_ID})
    print_response(response, f"Career Advice: {topic}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            print(f"✅ Advice Response:")
            print(f"{data['data']['response'][:500]}...")
            return True
    
    return False

def test_clear_history(session_id: str = SESSION_ID):
    """Test clearing conversation history"""
    print("\n🗑️  Testing Clear History...")
    
    payload = {"session_id": session_id}
    
    response = requests.delete(f"{API_BASE_URL}/history", json=payload)
    print_response(response, "Clear History")
    return response.status_code == 200

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🎓 AI Career Counselor API - Comprehensive Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Get Topics
    results.append(("Get Topics", test_get_topics()))
    
    # Test 3: Update Profile
    results.append(("Update Profile", test_update_profile()))
    
    # Test 4: Get Profile
    results.append(("Get Profile", test_get_profile()))
    
    # Test 5: Chat - General career question
    results.append(("Chat - Career Path", test_chat(
        "I'm a computer science graduate with 2 years of experience. What career paths should I consider?"
    )))
    
    # Test 6: Chat - Resume help
    results.append(("Chat - Resume Help", test_chat(
        "Can you help me improve my resume for software engineering positions?"
    )))
    
    # Test 7: Chat - Interview prep
    results.append(("Chat - Interview Prep", test_chat(
        "I have an interview for a senior developer position next week. How should I prepare?"
    )))
    
    # Test 8: Get specific advice
    results.append(("Get Advice - Skills", test_get_advice("skills")))
    
    # Test 9: Get History
    results.append(("Get History", test_get_history()))
    
    # Test 10: Clear History
    results.append(("Clear History", test_clear_history()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total

def interactive_mode():
    """Interactive mode for testing"""
    print("\n🎓 AI Career Counselor API - Interactive Mode")
    print("=" * 60)
    print("Commands:")
    print("  chat <message>  - Send a chat message")
    print("  profile         - Update profile")
    print("  history         - View history")
    print("  advice <topic>  - Get specific advice")
    print("  quit            - Exit")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command == "chat" and len(parts) > 1:
                test_chat(parts[1])
            elif command == "profile":
                test_update_profile()
            elif command == "history":
                test_get_history()
            elif command == "advice" and len(parts) > 1:
                test_get_advice(parts[1])
            elif command == "health":
                test_health_check()
            elif command == "topics":
                test_get_topics()
            else:
                print("❓ Unknown command. Try: chat, profile, history, advice, topics, health, quit")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Run comprehensive test
            success = run_comprehensive_test()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "interactive":
            # Run interactive mode
            interactive_mode()
        else:
            print("Usage:")
            print("  python test_client.py test         - Run comprehensive tests")
            print("  python test_client.py interactive  - Interactive testing mode")
    else:
        # Default: run a quick test
        print("🎓 Running Quick Test...")
        print("\nTesting basic functionality:")
        test_health_check()
        test_chat("What skills should I learn as a beginner developer?")
        
        print("\n💡 Tip: Run with 'test' argument for comprehensive tests")
        print("        Run with 'interactive' for interactive mode")

if __name__ == "__main__":
    main()