from extensions import mysql
from utils.helpers import format_datetime, parse_image_urls
import json

def get_all_qna(page=1, per_page=10, keyword=''):
    offset = (page - 1) * per_page
    cur = mysql.connection.cursor()

    if keyword:
        # ✅ 검색어 있을 때 (취약하게)
        keyword_pattern = f"%{keyword}%"

        # 문자열 직접 삽입 (매우 위험)
        query_count = f"""
            SELECT COUNT(*) as count
            FROM qna
            WHERE title LIKE '{keyword_pattern}' OR comment LIKE '{keyword_pattern}'
        """
        cur.execute(query_count)
        total_count = cur.fetchone()['count']

        query_list = f"""
            SELECT q.id, q.user_id, q.title, q.comment, q.image_urls, q.writer, q.created_at
            FROM qna q
            WHERE q.title LIKE '{keyword_pattern}' OR q.comment LIKE '{keyword_pattern}'
            ORDER BY q.created_at DESC
            LIMIT {per_page} OFFSET {offset}
        """
        cur.execute(query_list)
    else:
        cur.execute("SELECT COUNT(*) as count FROM qna")
        total_count = cur.fetchone()['count']

        cur.execute(f"""
            SELECT q.id, q.user_id, q.title, q.comment, q.image_urls, q.writer, q.created_at
            FROM qna q
            ORDER BY q.created_at DESC
            LIMIT {per_page} OFFSET {offset}
        """)
        
    qna_list = cur.fetchall()

    # ✅ 디버깅: 전체 게시글 리스트 출력
    print("✅ [DEBUG] 가져온 Q&A 목록:")
    for item in qna_list:
        item['created_at'] = format_datetime(item.get('created_at'))
        item['image_urls'] = parse_image_urls(item.get('image_urls'))
        print(f" - ID: {item['id']}, Title: {item['title']}, Writer: {item.get('writer')}")

    cur.close()
    return qna_list, total_count

def get_qna_by_id(post_id):
    """
    ID로 Q&A 상세 조회
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT q.id, q.user_id, q.title, q.comment, q.image_urls, q.writer, q.created_at
        FROM qna q
        WHERE q.id = %s
    """, (post_id,))
    qna = cur.fetchone()
    cur.close()

    if qna:
        qna['created_at'] = format_datetime(qna.get('created_at'))
        qna['image_urls'] = parse_image_urls(qna.get('image_urls'))

        # ✅ 디버깅: 상세 글 출력
        print(f"✅ [DEBUG] Q&A 상세 조회 - ID: {qna['id']}, Writer: {qna.get('writer')}, Title: {qna['title']}")

    return qna

def create_qna(title, comment, image_urls=None, user_id=None, writer='익명'):
    """
    Q&A 게시물 작성
    """
    try:
        image_urls_json = json.dumps(image_urls) if image_urls else '[]'
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO qna (user_id, title, comment, image_urls, writer, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (user_id, title, comment, image_urls_json, writer))

        mysql.connection.commit()
        post_id = cur.lastrowid
        cur.close()

        print("✅ QNA INSERT 성공. post_id:", post_id, "/ 작성자:", writer)
        return post_id
    except Exception as e:
        print("💥 QNA INSERT ERROR:", str(e))
        return None

def delete_qna(post_id):
    """
    Q&A 게시물 삭제
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM qna WHERE id = %s", (post_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()

    print(f"🗑️ QNA DELETE 요청 - post_id: {post_id}, 성공 여부: {affected_rows > 0}")
    return affected_rows > 0
