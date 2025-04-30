from extensions import mysql
from utils.helpers import format_datetime, parse_image_urls
import json

def get_all_qna(page=1, per_page=10, keyword=''):
    offset = (page - 1) * per_page
    cur = mysql.connection.cursor()

    if keyword:
        # 인코딩된 keyword가 곧바로 SQL로 들어감
        # 예: %' UNION SELECT ... --
        query = f"""
            SELECT id, user_id, title, comment, image_urls, writer, created_at
            FROM qna
            WHERE title LIKE '%{keyword}%'
            ORDER BY created_at DESC
            LIMIT {per_page} OFFSET {offset}
        """
        print(f"[DEBUG] SQL 쿼리:\n{query}")
        cur.execute(query)

        qna_list = cur.fetchall()

        # 총 개수는 페이로드가 이미 LIMIT 포함하므로 생략하거나 가짜값
        total_count = len(qna_list)

    else:
        cur.execute("SELECT COUNT(*) as count FROM qna")
        total_count = cur.fetchone()['count']

        cur.execute(f"""
            SELECT id, user_id, title, comment, image_urls, writer, created_at
            FROM qna
            ORDER BY created_at DESC
            LIMIT {per_page} OFFSET {offset}
        """)
        qna_list = cur.fetchall()

    # 정리 및 반환
    for item in qna_list:
        item['created_at'] = format_datetime(item.get('created_at'))
        item['image_urls'] = parse_image_urls(item.get('image_urls'))
    cur.close()
    return qna_list, total_count

def get_qna_by_id(post_id):
    """
    ID로 Q&A 상세 조회 (유니온 인젝션 대응용)
    """
    cur = mysql.connection.cursor()

    # 문자열 삽입 허용 (인젝션용 테스트)
    query = f"""
        SELECT title, writer, created_at, comment
        FROM qna
        WHERE id = {post_id}
    """
    cur.execute(query)

    rows = cur.fetchall()
    cur.close()

    if rows and len(rows) > 0:
        qna = rows[0]  # 첫 번째 결과를 수동으로 꺼냄
        qna['created_at'] = format_datetime(qna.get('created_at'))

        print(f"✅ [DEBUG] Q&A 상세 조회 (UNION OK) - title: {qna['title']}, writer: {qna['writer']}")
        return qna
    else:
        print("❌ [DEBUG] 결과 없음")
        return None



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
