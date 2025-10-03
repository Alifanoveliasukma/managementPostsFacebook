from flask import Blueprint, request, jsonify, current_app
from extensions import db
from werkzeug.utils import secure_filename
from models.group import Group
import os

# Buat Blueprint untuk grup
groups_bp = Blueprint("groups", __name__)

def allowed_file(filename):
    allowed = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

# ========================
# GET semua grup
# ========================
@groups_bp.route("/", methods=["GET"])
def get_groups():
    groups = Group.query.all()
    return jsonify([g.to_dict() for g in groups])

# ========================
# POST tambah grup
# ========================
@groups_bp.route("/", methods=["POST"])

def add_group():
    name = request.form.get("name")
    fb_group_id = request.form.get("fb_group_id")
    description = request.form.get("description", "")
    rules = request.form.get("rules", "")
    
    # Ambil objek file yang diunggah
    uploaded_file = request.files.get("icon_url") 

    existing = Group.query.filter_by(fb_group_id=fb_group_id).first()
    if existing:
        return jsonify({"error": "ID sama!"}), 400
    
    # Inisialisasi path URL untuk DB
    icon_url_path = None 
    
    # Cek apakah file diunggah dan ekstensinya diizinkan
    if uploaded_file and allowed_file(uploaded_file.filename):
        # Proses menyimpan file
        filename = secure_filename(uploaded_file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        uploaded_file.save(save_path)
        
        # Simpan path URL publik yang akan digunakan di HTML
        icon_url_path = f"/static/uploads/{filename}" 

    new_group = Group(
        name=name,
        fb_group_id=fb_group_id,
        description=description,
        rules=rules,
        # Gunakan variabel path yang sudah diproses
        icon_url=icon_url_path 
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group added successfully"}), 201
# ========================
# PUT edit grup
# ========================
@groups_bp.route("/<int:id>", methods=["PUT"])
def edit_group(id):
    group = Group.query.get_or_404(id) # cari row by ID

    name = request.form.get("name")
    fb_group_id = request.form.get("fb_group_id")
    description = request.form.get("description", "")
    rules = request.form.get("rules", "")
    icon_url = request.files.get("icon_url")

    if name:
        group.name = name
    if fb_group_id:
        group.fb_group_id = fb_group_id
    if description:
        group.description = description
    if rules:
        group.rules = rules

    if icon_url and allowed_file(icon_url.filename):
        filename = secure_filename(icon_url.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        icon_url.save(save_path)
        group.icon_url = f"/static/uploads/{filename}"

    db.session.commit()
    return jsonify({"message": "Group updated successfully"})   

# ========================
# DELETE hapus grup
# ========================
@groups_bp.route("/<int:id>", methods=["DELETE"])
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return jsonify({"message": "Group deleted successfully"})
