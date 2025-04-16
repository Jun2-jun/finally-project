from flask import Flask, render_template, redirect, url_for, session
from modules.connection import mysql, init_db
from routes.auth import auth_bp
from routes.reservation import reserve_bp
from datetime import datetime




app = Flask(__name__)
init_db(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(reserve_bp, url_prefix="/api")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/reserve')
def reserve():
    return render_template("reserve.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", now=datetime.now())

@app.route('/find')
def find():
    return render_template("find.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

