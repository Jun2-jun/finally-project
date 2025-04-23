from flask import request, jsonify, current_app
from . import api_bp
from models.notice import get_all_notices, get_notice_by_id, create_notice, delete_notice
from utils.helpers import save_uploaded_files, paginate_results
from utils.auth import admin_required
from flask import session

# 공지사항 전체 목록 조회
@api_bp.route('/notices', methods=['GET'])
def get_notices_api():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        notices, total_count = get_all_notices(page, per_page)
        
        return jsonify({
            'status': 'success',
            'data': paginate_results(notices, page, per_page, total_count)
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 상세 조회
@api_bp.route('/notices/<int:post_id>', methods=['GET'])
def get_notice_detail_api(post_id):
    try:
        notice = get_notice_by_id(post_id)

        if not notice:
            return jsonify({
                'status': 'fail',
                'message': '공지사항을 찾을 수 없습니다.'
            }), 404

        return jsonify({
            'status': 'success',
            'data': notice
        })
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 상세 조회 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 작성 - JSON 또는 폼 데이터 둘 다 지원
@api_bp.route('/notices', methods=['POST'])
@admin_required
def create_notice_api():
    try:
        # 로그인한 관리자의 user_id 가져오기
        user_id = session.get('user_id')
        
        # JSON 또는 폼 데이터 처리
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            comment = data.get('comment')
            image_urls = []  # JSON 요청에서는 이미지를 처리하지 않음
        else:
            title = request.form.get('title')
            comment = request.form.get('comment')
            
            # 이미지 파일 처리
            files = request.files.getlist('images')
            upload_folder = current_app.config['UPLOAD_FOLDER']
            image_urls = save_uploaded_files(files, upload_folder)

        if not title or not comment:
            return jsonify({
                'status': 'fail', 
                'message': '제목과 내용을 입력해주세요.'
            }), 400

        # 공지사항 생성 시 user_id 전달
        notice_id = create_notice(title, comment, image_urls, user_id)

        return jsonify({
            'status': 'success', 
            'message': '공지사항이 등록되었습니다.',
            'data': {
                'notice_id': notice_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 등록 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 삭제
@api_bp.route('/notices/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_notice_api(post_id):
    try:
        success = delete_notice(post_id)

        if success:
            return jsonify({
                'status': 'success',
                'message': f'{post_id}번 공지사항이 삭제되었습니다.'
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': '해당 ID의 공지사항이 존재하지 않습니다.'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': f'공지사항 삭제 중 오류가 발생했습니다: {str(e)}'
        }), 500

# 공지사항 삭제 (POST 대체 - 클라이언트에서 DELETE를 지원하지 않는 경우)
@api_bp.route('/notices/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete_notice_post_api(post_id):
    return delete_notice_api(post_id)