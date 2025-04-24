from extensions import mysql
from utils.helpers import format_datetime, parse_image_urls
import json

def get_all_qna(page=1, per_page=10):
    """
    페이지네이션이, 적용된 모든 Q&A 게시물 가져오기
    """
    offset = (page - 1) * per_page
    
    cur = mysql.connection.cursor()
    
    # 전체 개수 가져오기
    cur.execute("SELECT COUNT(*) as count FROM qna")
    total_count = cur.fetchone()['count']
    
    # 페이지 데이터 가져오기 (사용자 정보 포함)
    cur.execute("""
        SELECT q.id, q.user_id, q.title, q.comment, q.image_urls, q.created_at, 
               u.username as author
        FROM qna q
        LEFT JOIN users u ON q.user_id = u.id
        ORDER BY q.created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    qna_list = cur.fetchall()
    cur.close()
    
    # 데이터 형식 변환
    for item in qna_list:
        item['created_at'] = format_datetime(item.get('created_at'))
        item['image_urls'] = parse_image_urls(item.get('image_urls'))
    
    return qna_list, total_count

def get_qna_by_id(post_id):
    """
    ID로 특정 Q&A 게시물 가져오기
    """
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT q.id, q.user_id, q.title, q.comment, q.image_urls, q.created_at, 
               u.username as author
        FROM qna q
        LEFT JOIN users u ON q.user_id = u.id
        WHERE q.id = %s
    """, (post_id,))
    qna = cur.fetchone()
    cur.close()
    
    if qna:
        qna['created_at'] = format_datetime(qna.get('created_at'))
        qna['image_urls'] = parse_image_urls(qna.get('image_urls'))
    
    return qna

def create_qna(title, comment, image_urls=None, category='일반', user_id=None):
    """
    새 Q&A 게시물 생성하기
    """
    try:
        image_urls_json = json.dumps(image_urls) if image_urls else '[]'
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO qna (user_id, title, comment, image_urls, category, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (user_id, title, comment, image_urls_json, category))

        mysql.connection.commit()
        post_id = cur.lastrowid
        cur.close()

        print("✅ QNA INSERT 성공. post_id:", post_id)
        return post_id
    except Exception as e:
        print("💥 QNA INSERT ERROR:", str(e))
        return None

def delete_qna(post_id):
    """
    Q&A 게시물 삭제하기
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM qna WHERE id = %s", (post_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    return affected_rows > 0