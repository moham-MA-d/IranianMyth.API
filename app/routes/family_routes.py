from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Family

family_bp = Blueprint('family_bp', __name__)

@family_bp.route("/", methods=["POST"])
def create_family():
    data = request.json
    
    if data is None:
       return jsonify({"error": "Invalid or missing JSON in request body"}), 400
   
    new_family = Family(
        id=data.get("id"),
        title=data.get("title"),
        imageProfile=data.get("imageProfile"),
        imageBg=data.get("imageBg"),
        description=data.get("description")
    )
    db.session.add(new_family)
    db.session.commit()
    return jsonify({"message": "Family created successfully", "id": new_family.id}), 201

@family_bp.route("/", methods=["GET"])
def get_all_families():
    families = Family.query.all()
    return jsonify([
        {
            "id": family.id,
            "title": family.title,
            "imageProfile": family.imageProfile,
            "imageBg": family.imageBg,
            "description": family.description
        }
        for family in families
    ])

@family_bp.route("/<string:id>", methods=["GET"])
def get_family(id):
    family = Family.query.get_or_404(id)
    return jsonify({
        "id": family.id,
        "title": family.title,
        "imageProfile": family.imageProfile,
        "imageBg": family.imageBg,
        "description": family.description
    })

@family_bp.route("/<string:id>", methods=["PUT"])
def update_family(id):
    family = Family.query.get_or_404(id)
    data = request.json
    
    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400
   
    family.title = data.get("title", family.title)
    family.imageProfile = data.get("imageProfile", family.imageProfile)
    family.imageBg = data.get("imageBg", family.imageBg)
    family.description = data.get("description", family.description)
    db.session.commit()
    return jsonify({"message": "Family updated successfully"})

    

@family_bp.route("/<string:id>", methods=["DELETE"])
def delete_family(id):
    family = Family.query.get_or_404(id)
    db.session.delete(family)
    db.session.commit()
    return jsonify({"message": "Family deleted successfully"})