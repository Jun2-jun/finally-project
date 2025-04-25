from flask import Blueprint, request, jsonify, session, current_app
from models.qna import get_all_qna, get_qna_by_id, create_qna, delete_qna
from utils.helpers import save_uploaded_files, paginate_results
from utils.auth import login_required, admin_required

# ✅ Q&A 전용 Blueprint 정의
qna_bp = Blueprint('qna', __name__, url_prefix='/api/qna')

# 1. Q&A 목록 조회
@qna_bp.route('/', methods=['GET'])
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
        return jsonify({'status': 'fail', 'message': f'Q&A 목록 오류: {str(e)}'}), 500

# 2. Q&A 상세 조회
@qna_bp.route('/<int:post_id>', methods=['GET'])
def get_qna_detail_api(post_id):
    try:
        qna = get_qna_by_id(post_id)
        if not qna:
            return jsonify({'status': 'fail', 'message': '게시글이 없습니다.'}), 404
        return jsonify({'status': 'success', 'data': qna})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Q&A 상세 조회 오류: {str(e)}'}), 500

# 3. Q&A 작성 (작성자 자동 설정 포함)
@qna_bp.route('/', methods=['POST'])
@login_required
def create_qna_api():
    try:
        user_id = session.get('user_id')
        writer = session.get('username') or session.get('user', {}).get('username', '익명')

        # 🔍 디버깅용 로그 출력
        print("✅ [QNA] 세션 사용자 ID:", user_id)
        print("✅ [QNA] 세션 작성자 이름:", writer)
        print("✅ [QNA] 세션 전체 내용:", dict(session))

        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            comment = data.get('comment')
            category = data.get('category', '일반')
            image_urls = []
        else:
            title = request.form.get('title')
            comment = request.form.get('comment')
            category = request.form.get('category', '일반')
            files = request.files.getlist("images")
            image_urls = save_uploaded_files(files, current_app.config['UPLOAD_FOLDER'])

        if not title or not comment:
            return jsonify({'status': 'fail', 'message': '제목과 내용을 입력해주세요.'}), 400

        post_id = create_qna(
            title=title,
            comment=comment,
            image_urls=image_urls,
            user_id=user_id,
            writer=writer
        )

        return jsonify({
            'status': 'success',
            'message': 'Q&A가 등록되었습니다.',
            'data': {'post_id': post_id}
        }), 201
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Q&A 등록 오류: {str(e)}'}), 500

# 4. Q&A 삭제 (DELETE)
@qna_bp.route('/<int:post_id>', methods=['DELETE'])
@admin_required
def delete_qna_api(post_id):
    try:
        success = delete_qna(post_id)
        if success:
            return jsonify({'status': 'success', 'message': f'{post_id}번 Q&A 삭제됨'}), 200
        else:
            return jsonify({'status': 'fail', 'message': '해당 Q&A가 존재하지 않음'}), 404
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Q&A 삭제 오류: {str(e)}'}), 500

# 5. Q&A 삭제 (POST 대체)
@qna_bp.route('/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete_qna_post_api(post_id):
    return delete_qna_api(post_id)

# 6. 추가 경로 호환성 대응
@qna_bp.route('/posts', methods=['GET'])
def get_posts():
    return get_qna_api()

@qna_bp.route('/posts', methods=['POST'])
def create_post():
    return create_qna_api()
