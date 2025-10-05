from flask import Blueprint, request, jsonify
from extensions import db
from models.post import Post
from models.group import Group

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {"id": p.id, 
         "title": p.title, 
         "content": p.content,
         "groups": [g.name for g in p.groups]
         } for p in posts
    ])

@posts_bp.route("/", methods=["POST"])
def add_post():
    title = request.form.get("title")
    content = request.form.get("content")

    new_post = Post(
        title=title,
        content=content,
    )

    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post Setting successfully"})

@posts_bp.route("/<int:id>", methods=["PUT"])
def edit_post(id):
    post = Post.query.get_or_404(id)

    title = request.form.get("title")
    content = request.form.get("content")

    if title:
        post.title = title
    if content:
        post.content = content

    db.session.commit()
    return jsonify({"message": "Post updated successfully"})

@posts_bp.route("/<int:id>", methods=["GET"]) # <--- TAMBAHKAN DECORATOR INI
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "groups": [g.name for g in post.groups]
    })

@posts_bp.route("/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"})

@posts_bp.route("/<int:id>/assign", methods=["PUT"])
def assign_post_to_groups(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    group_ids = data.get("group_ids", [])

    # reset relasi lama, assign baru
    post.groups = []
    for gid in group_ids:
        group = Group.query.get(gid)
        if group:
            post.groups.append(group)

    db.session.commit()
    return jsonify({"message": "Post linked to groups"})
