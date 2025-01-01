from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Myth

myth_bp = Blueprint('myth_bp', __name__)

@myth_bp.route('', methods=['GET'])
def get_all_myths():
    myths = Myth.query.all()
    return jsonify([
        {
            "id": myth.id,
            "name": myth.name,
            "nickname": myth.nickname,
            "age": myth.age,
            "era_id": myth.era_id,
        }
        for myth in myths
    ])

@myth_bp.route('/<int:id>', methods=['GET'])
def get_myth(id):
    myth = Myth.query.get_or_404(id)
    return jsonify({
        "id": myth.id,
        "name": myth.name,
        "nickname": myth.nickname,
        "age": myth.age,
        "era_id": myth.era_id,
    })

@myth_bp.route('', methods=['POST'])
def create_myth():
    data = request.json

    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400

    new_myth = Myth(
        name=data.get("name"),
        nickname=data.get("nickname"),
        age=data.get("age"),
        era_id=data.get("era_id")
    )
    db.session.add(new_myth)
    db.session.commit()
    return jsonify({"message": "Myth created successfully", "id": new_myth.id}), 201

@myth_bp.route('/<int:id>', methods=['PUT'])
def update_myth(id):
    myth = Myth.query.get_or_404(id)
    data = request.json
    
    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400
    
    myth.name = data.get("name", myth.name)
    myth.nickname = data.get("nickname", myth.nickname)
    myth.age = data.get("age", myth.age)
    myth.era_id = data.get("era_id", myth.era_id)
    db.session.commit()
    return jsonify({"message": "Myth updated successfully"})

@myth_bp.route('/<int:id>', methods=['DELETE'])
def delete_myth(id):
    myth = Myth.query.get_or_404(id)
    db.session.delete(myth)
    db.session.commit()
    return jsonify({"message": "Myth deleted successfully"})


