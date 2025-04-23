from flask import request, jsonify
from . import api_bp
from utils.ai import call_gemini_api
import os

# AI 엔드포인트
@api_bp.route('/ai', methods=['POST'])
def gemini_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        api_key = data.get('api_key')  # 클라이언트에서 API 키 제공 또는 환경 변수에서 가져오기
        
        if not prompt:
            return jsonify({
                'status': 'fail',
                'message': '프롬프트가 필요합니다.'
            }), 400
            
        if not api_key:
            api_key = os.environ.get('GEMINI_API_KEY','api_key자리')  # 환경 변수에서 가져오기
            
        if not api_key:
            return jsonify({
                'status': 'fail',
                'message': 'API 키가 필요합니다.'
            }), 400
        
        # Gemini API 호출
        result = call_gemini_api(prompt, api_key)
        
        # 에러 처리
        if 'error' in result:
            return jsonify({
                'status': 'fail',
                'message': f'Gemini API 호출 중 오류가 발생했습니다: {result["error"]}'
            }), 500
        
        return jsonify({
            'status': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Gemini API 호출 중 오류가 발생했습니다: {str(e)}'
        }), 500