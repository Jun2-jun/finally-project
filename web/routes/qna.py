from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify
from datetime import datetime

qna_bp = Blueprint("qna", __name__, url_prefix="/qna")

posts = []

@qna_bp.route("/", methods=["GET"])
def qna_list():
    return render_template("qna/qna.html", posts=posts, now=datetime.now())

@qna_bp.route("/write", methods=["GET", "POST"])
def qna_write():
    if request.method == "POST":
        title = request.form.get("title")
        comment = request.form.get("comment")
        created_at = datetime.now()

        posts.append({
            "no": len(posts) + 1,
            "title": title,
            "content": comment,
            "category": "기타",
            "created_at": created_at.strftime("%Y-%m-%d %H:%M"),
            "views": 0
        })

        return redirect(url_for("qna.qna_list"))

    return render_template("qna/qna_write.html", now=datetime.now())

@qna_bp.route("/post/<int:post_id>", methods=["GET"])
def qna_post_detail(post_id):
    post = next((p for p in posts if p.get("no") == post_id), None)
    if not post:
        return "해당 게시글이 없습니다.", 404

    post["views"] += 1

    response = make_response(render_template("qna/qna_detail.html", post=post))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@qna_bp.route("/delete", methods=["POST"])
def qna_delete():
    to_delete = request.json.get("delete_ids", [])
    global posts
    posts = [p for p in posts if str(p["no"]) not in to_delete]
    return jsonify(success=True)
