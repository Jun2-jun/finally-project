from flask import Flask, render_template
from modules.db import init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp

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

if __name__ == '__main__':
    app.run(debug=True)
