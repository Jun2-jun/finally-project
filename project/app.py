from flask import Flask, render_template, request, redirect, url_for
from modules.db import init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp
from datetime import datetime

posts = []
next_id = 1

app = Flask(__name__)
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(reserve_bp, url_prefix="/api")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/reserve')
def reserve():
    return render_template("reserve.html")

@app.route('/notice')
def notice():
    return render_template("notice.html")

@app.route('/qna')
def  qna():
    return render_template("qna.html", posts=posts)

@app.route('/qna/post/<int:post_id>')
def qna_post_detail(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    return render_template("qna_detail.html", post=post)
    


@app.route('/qna/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return redirect(url_for('qna'))


@app.route('/qna/qnawrite', methods=['GET', 'POST'])
def qnawrite():
    global posts, next_id
    if request.method == 'POST':
        title = request.form.get('title')
        comment = request.form.get('comment')
        post = {
            'id': next_id,                 
            'no': next_id,                 
            'category': '일반',
            'title': title,
            'comment': comment,          
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        posts.insert(0, post)
        next_id += 1
        return redirect(url_for('qna'))

    return render_template("qnawrite.html")


@app.route('/qna/writedel')
def  writedel():
    return render_template("writedel.html")

if __name__ == '__main__':
    app.run(debug=True)
