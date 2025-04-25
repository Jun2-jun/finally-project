import requests
import os

def call_gemini_api(prompt):
    """
    Gemini API를 주어진 프롬프트로 호출
    """

    api_key = os.environ.get('GEMINI_API_KEY','AIzaSyCNNvCkXPWQGKghFa7gMNVF1FPZm5-0V00')  # 환경 변수에서 가져오기
    api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
    url = f"{api_url}?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # 의료정보만 대답하도록 프롬프트 작성
    medical_prompt = (
        "당신은 전문 의료 상담 AI입니다. 건강 정보, 증상, 약 복용, 생활 습관 개선과 관련된 질문에만 응답하세요. "
        "그 외의 질문에는 '이 서비스는 의료 정보 제공에만 특화되어 있습니다.'라고 답변하세요.\n\n"
        f"사용자 질문: {prompt}"
    )

    data = {
        "contents": [{
            "parts": [{"text": medical_prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
