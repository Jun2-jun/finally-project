from flask import request, jsonify
from . import api_bp
from models.qna import get_all_qna, get_qna_by_id, create_qna, delete_qna
from utils.helpers import save_uploaded_files, paginate_results
from utils.auth import login_required, admin_required
from flask import current_app
from flask import session

# Q&A 목록 조회
@api_bp.route('/qna', methods=['GET'])
def get_qna_api():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        qna_list, total_count = get_all_qna(page, per_page)
        
        return jsonify({
            'status': 'success',
            'data': paginate_results(qna_list, page, per_page, total_count)
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q&A 상세 조회
@api_bp.route('/qna/<int:post_id>', methods=['GET'])
def get_qna_detail_api(post_id):
    try:
        qna = get_qna_by_id(post_id)

        if not qna:
            return jsonify({
                'status': 'fail',
                'message': '게시글을 찾을 수 없습니다.'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': qna
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 상세 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q&A 작성 API - JSON 또는 폼 데이터 둘 다 지원
@api_bp.route('/qna', methods=['POST'])
def create_qna_api():
    try:
        # 로그인한 경우 user_id 가져오기
        user_id = session.get('user_id')
        
        # JSON 또는 폼 데이터 처리
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            comment = data.get('comment')
            category = data.get('category', '일반')
            image_urls = []  # JSON 요청에서는 이미지를 처리하지 않음
        else:
            title = request.form.get('title')
            comment = request.form.get('comment')
            category = request.form.get('category', '일반')
            
            # 이미지 파일 처리
            files = request.files.getlist("images")
            upload_folder = current_app.config['UPLOAD_FOLDER']
            image_urls = save_uploaded_files(files, upload_folder)

        if not title or not comment:
            return jsonify({
                'status': 'fail', 
                'message': '제목과 내용을 입력해주세요.'
            }), 400

        # Q&A 생성 시 user_id 전달
        post_id = create_qna(title, comment, image_urls, category, user_id)

        return jsonify({
            'status': 'success', 
            'message': 'Q&A가 등록되었습니다.',
            'data': {
                'post_id': post_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 등록 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q/A 삭제
@api_bp.route('/qna/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_qna_api(post_id):
    try:
        success = delete_qna(post_id)

        if success:
            return jsonify({
                'status': 'success',
                'message': f'{post_id}번 Q&A가 삭제되었습니다.'
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': '해당 ID의 Q&A가 존재하지 않습니다.'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'Q&A 삭제 중 오류가 발생했습니다: {str(e)}'
        }), 500

# Q/A 삭제 (POST 대체 - 클라이언트에서 DELETE를 지원하지 않는 경우)
@api_bp.route('/qna/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete_qna_post_api(post_id):
    return delete_qna_api(post_id)

# API 경로 추가 (앱 API URL과 일치시킴)
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    return get_qna_api()  # qna API와 동일한 기능

@api_bp.route('/posts', methods=['POST'])
def create_post():
    return create_qna_api()  # qna API와 동일한 기능