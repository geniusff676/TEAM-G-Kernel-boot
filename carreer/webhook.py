#!/usr/bin/env python3
"""
N8N Webhook Data Sender
Sends resume and job application data to n8n workflow
"""

import requests
import os
from pathlib import Path


def send_to_webhook(
    webhook_url: str,
    resume_path: str,
    title: str,
    experience: str,
    location: str,
    github: str,
    linkedin: str
):
    """
    Send job application data to n8n webhook
    
    Args:
        webhook_url: Full webhook URL
        resume_path: Path to PDF resume file
        title: Job title/role
        experience: Years of experience
        location: Preferred job location
        github: GitHub profile URL
        linkedin: LinkedIn profile URL
    
    Returns:
        Response object from the webhook
    """
    
    # Validate resume file exists
    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"Resume file not found: {resume_path}")
    
    # Prepare the multipart form data
    files = {
        'resume': (
            Path(resume_path).name,
            open(resume_path, 'rb'),
            'application/pdf'
        )
    }
    
    data = {
        'title': title,
        'experience': experience,
        'location': location,
        'github': github,
        'linkedin': linkedin
    }
    
    try:
        print(f"Sending data to webhook: {webhook_url}")
        print(f"Resume: {resume_path}")
        print(f"Job Details: {title} | {experience} years | {location}")
        
        response = requests.post(
            webhook_url,
            files=files,
            data=data,
            timeout=300  # 5 minutes timeout for processing
        )
        
        # Check response
        response.raise_for_status()
        
        print(f"\n✅ Success! Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")  # Print first 500 chars
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error sending data: {e}")
        raise
    
    finally:
        # Close the file
        files['resume'][1].close()


def main():
    """Main execution function with example usage"""
    
    # Configuration
    WEBHOOK_URL = "http://localhost:5678/webhook-test/acbef742-9d51-4d52-bca0-c1bc5c9104b0"
    # Job application details
    config = {
        'resume_path': '/home/eveevolve/chatan/output.pdf',
        'title': 'Software Engineer',
        'experience': '2',
        'location': 'Bangalore',
        'github': 'https://github.com/username',
        'linkedin': 'https://linkedin.com/in/username'
    }
    
    # Send to webhook
    try:
        response = send_to_webhook(WEBHOOK_URL, **config)
        print(f"\n📊 Workflow triggered successfully!")
        
    except Exception as e:
        print(f"\n⚠️ Failed to trigger workflow: {e}")
        exit(1)


if __name__ == "__main__":
    main()