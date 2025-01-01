from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Era

era_bp = Blueprint('era_bp', __name__)

@era_bp.route("/eras", methods=["POST"])
def create_era():
    data = request.json
    
    if data is None:
       return jsonify({"error": "Invalid or missing JSON in request body"}), 400
   
    new_era = Era(
        name=data.get("name"),
        image=data.get("image"),
        color=data.get("color"),
        description=data.get("description")
    )
    db.session.add(new_era)
    db.session.commit()
    return jsonify({"message": "Era created successfully", "id": new_era.id}), 201



@era_bp.route("/eras", methods=["GET"])
def get_all_eras():
    eras = Era.query.all()
    return jsonify([
        {
            "id": era.id,
            "name": era.name,
            "image": era.image,
            "color": era.color,
            "description": era.description
        }
        for era in eras
    ])

@era_bp.route("/eras/<int:id>", methods=["GET"])
def get_era(id):
    era = Era.query.get_or_404(id)
    return jsonify({
        "id": era.id,
        "name": era.name,
        "image": era.image,
        "color": era.color,
        "description": era.description
    })

@era_bp.route("/eras/<int:id>", methods=["PUT"])
def update_era(id):
    era = Era.query.get_or_404(id)
    data = request.json
    
    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400
   
    era.name = data.get("name", era.name)
    era.image = data.get("image", era.image)
    era.color = data.get("color", era.color)
    era.description = data.get("description", era.description)
    db.session.commit()
    return jsonify({"message": "Era updated successfully"})


@era_bp.route("/eras/<int:id>", methods=["DELETE"])
def delete_era(id):
    era = Era.query.get_or_404(id)
    db.session.delete(era)
    db.session.commit()
    return jsonify({"message": "Era deleted successfully"})