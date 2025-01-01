from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Myth, MythPhoto

myth_photos_bp = Blueprint('myth_photos_bp', __name__)

@myth_photos_bp.route("/myth_photos", methods=["POST"])
def create_myth_photo():
    data = request.json

    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400
    
    # Validate myth_id exists
    if not Myth.query.get(data.get("myth_id")):
        return jsonify({"error": "Invalid myth_id"}), 400

    new_photo = MythPhoto(
        myth_id=data.get("myth_id"),
        url=data.get("url"),
        title=data.get("title"),
        description=data.get("description")
    )
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({"message": "Myth photo created successfully", "id": new_photo.id}), 201

@myth_photos_bp.route("/myth_photos", methods=["GET"])
def get_all_myth_photos():
    photos = MythPhoto.query.all()
    return jsonify([
        {
            "id": photo.id,
            "myth_id": photo.myth_id,
            "url": photo.url,
            "title": photo.title,
            "description": photo.description
        }
        for photo in photos
    ])

@myth_photos_bp.route("/myths/<int:myth_id>/photos", methods=["GET"])
def get_photos_for_myth(myth_id):
    # Validate myth_id exists
    if not Myth.query.get(myth_id):
        return jsonify({"error": "Invalid myth_id"}), 404

    photos = MythPhoto.query.filter_by(myth_id=myth_id).all()
    return jsonify([
        {
            "id": photo.id,
            "url": photo.url,
            "title": photo.title,
            "description": photo.description
        }
        for photo in photos
    ])

@myth_photos_bp.route("/myth_photos/<int:id>", methods=["GET"])
def get_myth_photo(id):
    photo = MythPhoto.query.get_or_404(id)
    return jsonify({
        "id": photo.id,
        "myth_id": photo.myth_id,
        "url": photo.url,
        "title": photo.title,
        "description": photo.description
    })

@myth_photos_bp.route("/myth_photos/<int:id>", methods=["PUT"])
def update_myth_photo(id):
    photo = MythPhoto.query.get_or_404(id)
    data = request.json
    
    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400
    
    # Validate myth_id if updated
    if data.get("myth_id") and not Myth.query.get(data.get("myth_id")):
        return jsonify({"error": "Invalid myth_id"}), 400

    photo.myth_id = data.get("myth_id", photo.myth_id)
    photo.url = data.get("url", photo.url)
    photo.title = data.get("title", photo.title)
    photo.description = data.get("description", photo.description)
    db.session.commit()
    return jsonify({"message": "Myth photo updated successfully"})

@myth_photos_bp.route("/myth_photos/<int:id>", methods=["DELETE"])
def delete_myth_photo(id):
    photo = MythPhoto.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({"message": "Myth photo deleted successfully"})