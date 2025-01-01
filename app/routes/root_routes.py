from flask import Blueprint, request, jsonify
from sqlalchemy import null, true
from app.models import Myth, Era, ParentChild, Relationship, relationship
from app.extensions import db

root_bp = Blueprint('root_bp', __name__)


@root_bp.route("", methods=["GET"])
def get_diagram_data():
    # Fetch all eras and their related myths

    nodes = []

    default = {
        "id": 'poolx',
        "key": 'poolx',
        "loc": "10 20",
        "name": 'pool',
        "nickname": 'pool',
        "age": 0,
        "gender": "",
        "era_id": '',
        "era_name": '',
        "isGroup": True,
        "category": "pool"
    }
    nodes.append(default)

    allEra = Era.query.order_by(Era.order).all()
    # Loop through each era
    for era in allEra:
        # Add the era as a node
        e = {
            "id": era.id,
            "key": era.id,
            "loc": "30 80",
            "name": era.name,
            "nickname": era.name,
            "age": 0,
            "gender": "",
            "era_id": '',
            "era_name": '',
            "isGroup": True,
            "category": "Lane",
            "order": era.order,
            "group": "poolx"  # Group set to "basic" for era nodes
        }
        nodes.append(e)

        # Query myths that belong to the current era
        myths_in_era = Myth.query.filter_by(era_id=era.id).all()

        # Add each myth as a node
        for myth in myths_in_era:
            m = {
                "id": myth.id,
                "key": myth.id,
                "loc": myth.pos,
                "name": myth.name,
                "nickname": myth.nickname,
                "age": myth.age,
                "gender": myth.gender,
                "era_name": myth.era.name,
                "description": myth.description,
                "era_id": myth.era_id,
                "family_id": myth.family_id,
                "category_id": myth.category_id,
                "group": myth.era.id  # Group set to the era's name for myth nodes
            }
            nodes.append(m)

    # Fetch all parent-child links
    parent_child_links = [
        {
            "from": pc.parent_id,
            "to": pc.child_id,
            "relation": pc.relation_type,
            "color": pc.color,
            "description": pc.description
        }
        for pc in ParentChild.query.all()
    ]

    # Fetch all relationships (e.g., marriage, friendship)
    relationship_links = [
        {
            "id": rel.id,
            "from": rel.myth1_id,
            "to": rel.myth2_id,
            "relation": rel.relation_type,
            "description": rel.description
        }
        for rel in Relationship.query.all()
    ]

    # Combine all links
    links = parent_child_links + relationship_links

    # Return JSON response
    return jsonify({"nodes": nodes, "links": links})


@root_bp.route("/copyNode", methods=["POST"])
def copy_node():
    data = request.get_json()  # Get the JSON payload
    if data and 'node' in data:
        node = data['node']  # Access the 'node' dictionary

        # Create a new Myth object using the fields from the node
        new_myth = Myth(
            id=node['id'] + '1',
            name=node['name'],
            nickname=node['nickname'],
            pos=node['loc'],  # Assuming 'loc' maps to 'pos'
            age=node['age'],
            gender=node['gender'],
            era_id=node['era_id'],
            # Use .get() in case 'category_id' is missing
            category_id=node.get('category_id'),
            # Use .get() in case 'family_id' is missing
            family_id=node.get('family_id')
        )

        # Save the new myth to the database
        db.session.add(new_myth)
        db.session.commit()

        return jsonify({"isSuccess": True, "message": "Node copied successfully!"}), 200
    else:
        return jsonify({"isSuccess": False, "message": "Invalid data provided"}), 200


@root_bp.route("/moveNode", methods=["PUT"])
def move_node():
    data = request.get_json()
    id = data.get("id")
    pos = data.get("loc")

    if not id or not pos:
        return jsonify({"isSuccess": False, "message": "Invalid input"}), 400

    try:
        myth = Myth.query.filter_by(id=id).first()

        if myth:
            myth.pos = pos
            db.session.commit()
            return jsonify({"isSuccess": True, "message": "Node location is updated successfully!"}), 200

        return jsonify({"isSuccess": False, "message": "Node not found"}), 404

    except Exception as e:
        return jsonify({"isSuccess": False, "message": f"An error occurred: {str(e)}"}), 500


@root_bp.route("/editNode", methods=["PUT"])
def edit_node():
    data = request.get_json()
    id = data.get("id")
    name = data.get("name")
    description = data.get("description")

    if not id or not name or not description:
        return jsonify({"isSuccess": False, "message": "Invalid input"}), 400

    try:
        myth = Myth.query.filter_by(id=id).first()

        if myth:
            myth.name = name
            myth.description = description
            db.session.commit()
            return jsonify({"isSuccess": True, "message": "Node info is updated successfully!"}), 200

        return jsonify({"isSuccess": False, "message": "Node not found"}), 404

    except Exception as e:
        return jsonify({"isSuccess": False, "message": f"An error occurred: {str(e)}"}), 500


@root_bp.route("/deleteNode", methods=["DELETE"])
def delete_node():
    id = request.get_json().get("id")
    myth = Myth.query.filter_by(id=id).first()

    if myth:
        db.session.delete(myth)
        db.session.commit()
        return jsonify({"isSuccess": True, "message": "Node is deleted successfully!"}), 200

    else:
        return jsonify({"isSuccess": False, "message": "Failed to delete the node"}), 200




@root_bp.route("/editLink", methods=["PUT"])
def edit_link():
    data = request.get_json()
    id = data.get("id")
    description = data.get("description")

    if not id or not description:
        return jsonify({"isSuccess": False, "message": "Invalid input"}), 400

    try:
        link = Relationship.query.filter_by(id=id).first()

        if link:
            link.description = description
            db.session.commit()
            return jsonify({"isSuccess": True, "message": "Link info is updated successfully!"}), 200

        return jsonify({"isSuccess": False, "message": "Link not found"}), 404

    except Exception as e:
        return jsonify({"isSuccess": False, "message": f"An error occurred: {str(e)}"}), 500

@root_bp.route("/deleteLink", methods=["DELETE"])
def delete_link():
    id = request.get_json().get("id")
    relationship = Relationship.query.filter_by(id=id).first()

    if relationship:
        db.session.delete(relationship)
        db.session.commit()
        return jsonify({"isSuccess": True, "message": "lind is deleted successfully!"}), 200

    else:
        return jsonify({"isSuccess": False, "message": "Failed to delete the link"}), 200


@root_bp.route('/saveDiagram', methods=['POST'])
def save_diagram():
    data = request.get_json()
    nodes = data.get("nodes", [])
    links = data.get("links", [])

    if not nodes:
        return jsonify({"error": "No nodes data provided"}), 400

    try:
        for node_data in nodes:
            node_id = node_data.get("id")
            new_loc = node_data.get("loc")

            # Fetch the existing node from the database
            node = Myth.query.filter_by(id=node_id).first()

            if node:
                node.pos = new_loc
                node.name = node_data.get("name")

        for link_data in links:
            link_id = link_data.get("id")

            # Fetch the existing node from the database
            link = Relationship.query.filter_by(id=link_id).first()

            if not link:
                link = Relationship()
                link.relation_type = link_data.get("relation")
                link.myth1_id = link_data.get("from")
                link.myth2_id = link_data.get("to")
                link.relation_status = "active"
                link.description = ""

            if link:
                if link_data.get("isDeleted") == True:
                    db.session.delete(link)
                    continue

                link.relation_type = link_data.get("relation")

        # Commit changes to the database
        db.session.commit()

        return jsonify({"status": "success", "message": "Node locations updated successfully!"}), 200

    except Exception as e:
        print("Error updating nodes:", e)
        db.session.rollback()
        return jsonify({"error": "Failed to update nodes"}), 500