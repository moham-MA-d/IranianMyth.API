from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import RelationType

relation_type_bp = Blueprint('relation_type_bp', __name__)

@relation_type_bp.route("/", methods=["POST"])
def create_relation_type():
    data = request.json
    
    if data is None:
       return jsonify({"error": "Invalid or missing JSON in request body"}), 400
   
    new_relation_type = RelationType(
        id=data.get("id"),
        name=data.get("name"),
        color=data.get("color")
    )
    db.session.add(new_relation_type)
    db.session.commit()
    return jsonify({"message": "RelationType created successfully", "id": new_relation_type.id}), 201

@relation_type_bp.route("/", methods=["GET"])
def get_all_relation_types():
    relation_types = RelationType.query.all()
    return jsonify([
        {
            "id": rt.id,
            "name": rt.name,
            "color": rt.color
        }
        for rt in relation_types
    ])

@relation_type_bp.route("/<string:id>", methods=["GET"])
def get_relation_type(id):
    rt = RelationType.query.get_or_404(id)
    return jsonify({
        "id": rt.id,
        "name": rt.name,
        "color": rt.color
    })

@relation_type_bp.route("/<string:id>", methods=["PUT"])
def update_relation_type(id):
    rt = RelationType.query.get_or_404(id)
    data = request.json
    
    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400
   
    rt.name = data.get("name", rt.name)
    rt.color = data.get("color", rt.color)
    db.session.commit()
    return jsonify({"message": "RelationType updated successfully"})

@relation_type_bp.route("/<string:id>", methods=["DELETE"])
def delete_relation_type(id):
    rt = RelationType.query.get_or_404(id)
    db.session.delete(rt)
    db.session.commit()
    return jsonify({"message": "RelationType deleted successfully"})