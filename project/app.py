from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from modules.db import init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp
from datetime import datetime
import os
from werkzeug.utils import secure_filename

posts = []
next_id = 1

app = Flask(__name__)
init_db(app)
app.secret_key = 'your-secret-key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(reserve_bp, url_prefix="/api")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/reserve')
def reserve():
    return render_template("reserve.html")

@app.route('/notice')
def notice():
    user = session.get('user')
    is_admin = user and user.get('role') == 'admin'

    #실제로 사용할 공지사항 리스트를 가져오는 로직 필요
    notices = []  # 임시: 실제는 DB에서 가져오도록 구현해야 함

    return render_template("notice.html", notices=notices, is_admin=is_admin)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        if userid == 'admin' and password == '1234':
            session['user'] = {'id': userid, 'role': 'admin'}
            return redirect(url_for('notice'))
        else:
            return '로그인 실패'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
    


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


@app.route('/qna/qna_write', methods=['GET', 'POST'])
def qna_write():
    global posts, next_id
    if request.method == 'POST':
        title = request.form.get('title')
        comment = request.form.get('comment')

        # 이미지 파일 수집
        image_urls = []
        for key in request.files:
            file = request.files[key]
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_urls.append('/' + filepath.replace('\\', '/'))  # URL용으로 변경

        post = {
            'id': next_id,
            'no': next_id,
            'category': '일반',
            'title': title,
            'comment': comment,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'images': image_urls  # 추가된 이미지 리스트
        }

        posts.insert(0, post)
        next_id += 1
        return redirect(url_for('qna'))

    return render_template("qna_write.html")



@app.route('/qna/qna_delbutton')
def  qna_delbutton():
    return render_template("qna_delbutton.html")

if __name__ == '__main__':
    app.run(debug=True)
