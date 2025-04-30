# api/notices.py

from flask import Blueprint, request, jsonify, session, current_app
from models.notice import get_all_notices, get_notice_by_id, create_notice, delete_notice
from utils.helpers import save_uploaded_files, paginate_results
from utils.auth import admin_required

# Blueprint 정의
notices_bp = Blueprint('notices', __name__, url_prefix='/api/notices')

# 1. 공지사항 전체 목록 조회
@notices_bp.route('/', methods=['GET'])
def get_notices_api():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))        
        keyword = request.args.get('keyword', '', type=str)

        notices, total_count = get_all_notices(page, per_page, keyword)

        return jsonify({
            'status': 'success',
            'data': paginate_results(notices, page, per_page, total_count)
        })
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'공지사항 목록 조회 오류: {str(e)}'}), 500

# 2. 공지사항 상세 조회
@notices_bp.route('/<int:post_id>', methods=['GET'])
def get_notice_detail_api(post_id):
    try:
        notice = get_notice_by_id(post_id)
        if not notice:
            return jsonify({'status': 'fail', 'message': '공지사항이 없습니다.'}), 404
        return jsonify({'status': 'success', 'data': notice})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'공지사항 상세 조회 오류: {str(e)}'}), 500

# 3. 공지사항 작성 (JSON or multipart 지원)
@notices_bp.route('/', methods=['POST'])
@admin_required
def create_notice_api():
    try:
        user_id = session.get('user_id')

        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            comment = data.get('comment')
            image_urls = data.get('image_urls', [])
        else:
            title = request.form.get('title')
            comment = request.form.get('comment')
            files = request.files.getlist('images')
            image_urls = save_uploaded_files(files, current_app.config['UPLOAD_FOLDER'])

        if not title or not comment:
            return jsonify({'status': 'fail', 'message': '제목과 내용을 입력해주세요.'}), 400

        notice_id = create_notice(title, comment, image_urls, user_id)
        return jsonify({
            'status': 'success',
            'message': '공지사항 등록 완료',
            'data': {'notice_id': notice_id},
            'session' : session.sid
        }), 201
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'공지사항 등록 오류: {str(e)}'}), 500

# 4. 공지사항 삭제 (DELETE)
@notices_bp.route('/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_notice_api(post_id):
    try:
        success = delete_notice(post_id)
        if success:
            return jsonify({'status': 'success', 'message': f'{post_id}번 공지사항 삭제 완료'}), 200
        else:
            return jsonify({'status': 'fail', 'message': '공지사항이 존재하지 않습니다.'}), 404
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'삭제 중 오류 발생: {str(e)}'}), 500

# 5. 공지사항 삭제 (POST 대체용)
@notices_bp.route('/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete_notice_post_api(post_id):
    return delete_notice_api(post_id)
