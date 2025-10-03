import os
from flask import Flask, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from extensions import db 

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost:5432/fb_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Konfigurasi upload
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Inisialisasi database
db.init_app(app)
from models.group import Group
with app.app_context():
    db.create_all()

# Import dan register routes (Blueprint)
from routes.groups import groups_bp
app.register_blueprint(groups_bp, url_prefix="/groups")

# Route utama
@app.route("/")
def home():
    return render_template("index.html")

# Entry point
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)