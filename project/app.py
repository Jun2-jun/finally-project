from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from modules.db import init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp
from datetime import datetime
import os
from werkzeug.utils import secure_filename

posts = []
notices = []
next_qna_id = 1
next_notice_id = 1

app = Flask(__name__)
init_db(app)
app.secret_key = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

@app.route('/notice', methods=['GET', 'POST'])
def notice():
    global notices
    filtered_notices = notices
    start_date = ''
    end_date = ''
    query = ''

    if request.method == 'POST':
        start_date = request.form.get('startDate', '')
        end_date = request.form.get('endDate', '')
        query = request.form.get('query', '')

        if query:
            filtered_notices = [n for n in filtered_notices if query.lower() in n['title'].lower()]

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                filtered_notices = [
                    notice for notice in filtered_notices
                    if start <= datetime.strptime(notice['created_at'], '%Y-%m-%d %H:%M') <= end
                ]
            except ValueError:
                pass

    return render_template("notice.html", posts=filtered_notices,
                           start_date=start_date, end_date=end_date, query=query)

@app.route('/notice/post/<int:post_id>')
def notice_post_detail(post_id):
    post = next((p for p in notices if p['id'] == post_id), None)
    if not post:
        return "게시글을 찾을 수 없습니다.", 404
    post['views'] = post.get('views', 0) + 1
    return render_template("notice_detail.html", post=post)

@app.route('/notice/notice_write', methods=['GET', 'POST'])
def notice_write():
    global notices, next_notice_id
    if request.method == 'POST':
        title = request.form.get('title')
        comment = request.form.get('comment')

        image_urls = []
        for file in request.files.getlist('images'):
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_urls.append('/static/uploads/' + filename)

        # 반복문 바깥에서 게시글 생성 및 저장
        post = {
            'id': next_notice_id,
            'no': next_notice_id,
            'category': '일반',
            'title': title,
            'comment': comment,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'images': image_urls
        }

        notices.insert(0, post)
        next_notice_id += 1
        return redirect(url_for('notice'))

    return render_template("notice_write.html")

@app.route('/notice/delete/<int:post_id>', methods=['POST'])
def delete_notice(post_id):
    global notices
    notices = [post for post in notices if post['id'] != post_id]
    return redirect(url_for('notice'))




@app.route('/qna')
def qna():
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
    global posts, next_qna_id
    if request.method == 'POST':
        title = request.form.get('title')
        comment = request.form.get('comment')

        image_urls = []
        files = request.files.getlist("images")
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_urls.append('/' + filepath.replace('\\', '/'))

        post = {
            'id': next_qna_id,
            'no': next_qna_id,
            'category': '일반',
            'title': title,
            'comment': comment,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'images': image_urls
        }

        posts.insert(0, post)
        next_qna_id += 1
        return redirect(url_for('qna'))

    return render_template("qna_write.html")

@app.route('/qna/qna_delbutton')
def qna_delbutton():
    return render_template("qna_delbutton.html")

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        url = url_for('static', filename='uploads/' + filename)  # ⭐ 여기를 꼭 이렇게 반환해야 브라우저에서 접근 가능
        return {'success': True, 'url': url}
    return {'success': False}, 400



if __name__ == '__main__':
    app.run(debug=True)