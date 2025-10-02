from flask import Blueprint, request, jsonify
from extensions import db
from models.group import Group

# Buat Blueprint untuk grup
groups_bp = Blueprint("groups", __name__)

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
    data = request.json
    new_group = Group(
        name=data["name"],
        fb_group_id=data["fb_group_id"],
        rules=data.get("rules", "")
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group added successfully"}), 201


# ========================
# PUT edit grup
# ========================
@groups_bp.route("/<int:id>", methods=["PUT"])
def edit_group(id):
    group = Group.query.get_or_404(id)
    data = request.json
    group.name = data.get("name", group.name)
    group.fb_group_id = data.get("fb_group_id", group.fb_group_id)
    group.rules = data.get("rules", group.rules)

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
