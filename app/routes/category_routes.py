from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Category

category_bp = Blueprint("category_bp", __name__)


@category_bp.route("/", methods=["POST"])
def create_category():
    data = request.json

    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400

    new_category = Category(
        id=data.get("id"),
        title=data.get("title"),
        imageProfile=data.get("imageProfile"),
        imageBg=data.get("imageBg"),
        description=data.get("description"),
    )
    db.session.add(new_category)
    db.session.commit()
    return (
        jsonify({"message": "Category created successfully", "id": new_category.id}),
        201,
    )


@category_bp.route("/", methods=["GET"])
def get_all_categories():
    categories = Category.query.all()
    return jsonify(
        [
            {
                "id": category.id,
                "title": category.title,
                "imageProfile": category.imageProfile,
                "imageBg": category.imageBg,
                "description": category.description,
            }
            for category in categories
        ]
    )


@category_bp.route("/<string:id>", methods=["GET"])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(
        {
            "id": category.id,
            "title": category.title,
            "imageProfile": category.imageProfile,
            "imageBg": category.imageBg,
            "description": category.description,
        }
    )


@category_bp.route("/<string:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.json

    if data is None:
        return jsonify({"error": "Invalid or missing JSON in request body"}), 400

    category.title = data.get("title", category.title)
    category.imageProfile = data.get("imageProfile", category.imageProfile)
    category.imageBg = data.get("imageBg", category.imageBg)
    category.description = data.get("description", category.description)
    db.session.commit()
    return jsonify({"message": "Category updated successfully"})


@category_bp.route("/<string:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"})
