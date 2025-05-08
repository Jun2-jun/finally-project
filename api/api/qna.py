from flask import Blueprint, request, jsonify, session, current_app
from models.qna import get_all_qna, get_qna_by_id, create_qna, delete_qna
from utils.helpers import save_uploaded_files, paginate_results
from utils.auth import login_required, admin_required
from extensions import mysql
from flask_mysqldb import MySQLdb
from collections import defaultdict

# Q&A 전용 Blueprint 정의
qna_bp = Blueprint('qna', __name__, url_prefix='/api/qna')

# 1. Q&A 목록 조회
@qna_bp.route('/', methods=['GET'])
def get_qna_api():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        keyword = request.args.get('keyword', '', type=str)

        qna_list, total_count = get_all_qna(page, per_page, keyword)

        return jsonify({
            'status': 'success',
            'data': paginate_results(qna_list, page, per_page, total_count)
        })
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'Q&A 목록 오류: {str(e)}'}), 500

# 2. Q&A 상세 조회
@qna_bp.route('/<int:post_id>', methods=['GET'])  # ✅ 정수형으로 수정
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
        print(" [QNA] 세션 사용자 ID:", user_id)
        print(" [QNA] 세션 작성자 이름:", writer)
        print(" [QNA] 세션 전체 내용:", dict(session))

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

@qna_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_qna_post_api(post_id):
    user_id = session.get('user_id')
    username = session.get('username')

    qna = get_qna_by_id(post_id)
    if not qna:
        return jsonify({'status': 'fail', 'message': '게시글이 존재하지 않습니다.'}), 404

    if qna['writer'] != username:
        return jsonify({'status': 'fail', 'message': '본인만 삭제할 수 있습니다.'}), 403

    success = delete_qna(post_id)
    if success:
        return jsonify({'status': 'success', 'message': f'{post_id}번 Q&A 삭제됨'}), 200
    else:
        return jsonify({'status': 'fail', 'message': '삭제 실패'}), 500


# 6. 추가 경로 호환성 대응
@qna_bp.route('/posts', methods=['GET'])
def get_posts():
    return get_qna_api()

@qna_bp.route('/posts', methods=['POST'])
def create_post():
    return create_qna_api()

# 댓글 등록 (parent_id 지원)
@qna_bp.route('/<int:qna_id>/comments', methods=['POST'])
def add_comment(qna_id):
    if 'user_id' not in session:
        return jsonify({'status': 'fail', 'message': '로그인 필요'}), 401

    comment = request.form.get('comment')
    parent_id = request.form.get('parent_id')  # FormData에서 받음
    user_id = session['user_id']

    if not comment:
        return jsonify({'status': 'fail', 'message': '댓글 내용이 없습니다'}), 400

    # 빈 문자열을 None으로 처리
    parent_id = int(parent_id) if parent_id not in [None, '', 'null'] else None

    try:
        cur = mysql.connection.cursor()
        if parent_id is not None:
            cur.execute("""
                INSERT INTO qna_comments (qna_id, user_id, comment, parent_id)
                VALUES (%s, %s, %s, %s)
            """, (qna_id, user_id, comment, parent_id))
        else:
            cur.execute("""
                INSERT INTO qna_comments (qna_id, user_id, comment)
                VALUES (%s, %s, %s)
            """, (qna_id, user_id, comment))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': '댓글 등록 완료'})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

# 댓글 조회 (DictCursor 사용)
@qna_bp.route('/<int:qna_id>/comments', methods=['GET'])
def get_comments(qna_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT qc.id, qc.comment, qc.created_at, qc.parent_id, u.username
        FROM qna_comments qc
        JOIN users u ON qc.user_id = u.id
        WHERE qc.qna_id = %s
        ORDER BY qc.created_at ASC
    """, (qna_id,))
    rows = cur.fetchall()
    cur.close()

    # 댓글을 id 기준으로 저장
    comment_map = {}
    for row in rows:
        comment_map[row['id']] = {
            'id': row['id'],
            'comment': row['comment'],
            'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M'),
            'parent_id': row['parent_id'],
            'username': row['username'],
            'replies': []
        }

    # 트리 구조 구성
    comment_tree = []
    for comment in comment_map.values():
        parent_id = comment['parent_id']
        if parent_id is None:
            comment_tree.append(comment)  # 최상위 댓글
        else:
            # 부모 댓글이 존재하면 replies에 추가
            parent = comment_map.get(parent_id)
            if parent:
                parent['replies'].append(comment)

    return jsonify(comment_tree)

# 대댓글
@qna_bp.route('/comments/<int:comment_id>/replies', methods=['GET'])
def get_replies(comment_id):
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT qc.id, qc.comment, qc.created_at, qc.parent_id, u.username
            FROM qna_comments qc
            JOIN users u ON qc.user_id = u.id
            WHERE qc.parent_id = %s
            ORDER BY qc.created_at ASC
        """, (comment_id,))
        rows = cur.fetchall()
        cur.close()

        replies = []
        for row in rows:
            replies.append({
                'id': row['id'],
                'comment': row['comment'],
                'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M'),
                'parent_id': row['parent_id'],
                'username': row['username'],
            })

        return jsonify({'status': 'success', 'data': replies})
    except Exception as e:
        return jsonify({'status': 'fail', 'message': f'대댓글 조회 오류: {str(e)}'}), 500
