from flask import Flask
from extensions import db 
from flask import render_template

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost:5432/fb_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
db.init_app(app)

# Import model supaya terdaftar di SQLAlchemy
from models.group import Group

# Create table kalau belum ada
with app.app_context():
    db.create_all()

# Import dan register routes (Blueprint)
from routes.groups import groups_bp
app.register_blueprint(groups_bp, url_prefix="/groups")

@app.route("/")
def home():
    return render_template("index.html")

# Entry point
if __name__ == "__main__":
    app.run(debug=True)
