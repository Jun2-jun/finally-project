# routes/notice.py
from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify
from datetime import datetime

# Blueprint 등록 (❗template_folder 제거)
notice_bp = Blueprint("notice", __name__)

# 메모리상 공지사항 데이터 저장소
notices = []

# 공지사항 목록 페이지
@notice_bp.route("/notice", methods=["GET"])
def notice_list():
    return render_template("notice/notice.html", posts=notices, now=datetime.now())

# 공지사항 작성 페이지
@notice_bp.route("/notice/notice_write", methods=["GET", "POST"])
def notice_write():
    if request.method == "POST":
        title = request.form.get("title")
        comment = request.form.get("comment")
        created_at = datetime.now()

        notices.append({
            "no": len(notices) + 1,
            "title": title,
            "content": comment,
            "writer": "관리자",
            "created_at": created_at.strftime("%Y-%m-%d %H:%M"),
            "views": 0
        })

        return redirect(url_for("notice.notice_list"))

    return render_template("notice/notice_write.html", now=datetime.now())

# 공지사항 상세 보기
@notice_bp.route("/notice/post/<int:post_id>", methods=["GET"])
def notice_post_detail(post_id):
    post = next((n for n in notices if n.get("no") == post_id), None)
    if not post:
        return "해당 공지사항이 없습니다.", 404

    post["views"] += 1

    response = make_response(render_template("notice/notice_detail.html", post=post))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# 선택된 공지사항 삭제
@notice_bp.route("/notice/delete", methods=["POST"])
def notice_delete():
    to_delete = request.json.get("delete_ids", [])
    global notices
    notices = [n for n in notices if str(n["no"]) not in to_delete]
    return jsonify(success=True)
