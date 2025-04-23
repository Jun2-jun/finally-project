import requests
import os

def call_gemini_api(prompt, api_key=None):
    """
    Gemini API를 주어진 프롬프트로 호출
    """
    if not api_key:
        api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyBwGAZB1xCnAW4XcWhY9ZhksBAxXyF5kvA')
    
    api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
    url = f"{api_url}?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}