from flask import Flask, render_template, request
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

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/find')
def find():
    return render_template("find.html")

@app.route('/reservation')
def reservation():
    hospital_name = request.args.get('place.place_name', '')
    hospital_address = request.args.get('place.address_name', '')
    return render_template('reservation.html', hospital_name=hospital_name, hospital_address=hospital_address)

if __name__ == '__main__':
    app.run(debug=True)
