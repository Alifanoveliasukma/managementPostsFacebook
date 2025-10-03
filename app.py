import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inisialisasi database
db.init_app(app)
from models.group import Group
with app.app_context():
    db.create_all()

# Import dan register routes (Blueprint)
from routes.groups import groups_bp
app.register_blueprint(groups_bp, url_prefix="/groups")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        file_url = url_for('static', filename=f'uploads/{filename}')
        return f"File berhasil diupload: <img src='{file_url}' width='200'>"

# Serve file upload biar bisa diakses
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Entry point
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
