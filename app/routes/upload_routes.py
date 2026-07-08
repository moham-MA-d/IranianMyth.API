"""Serves locally-stored uploaded media (see app.storage.LocalStorage).

MythPhoto.url / Myth.imageProfile hold relative paths like
``uploads/myths/<myth_id>/<name>.jpg``; the web frontend resolves them against
the API base URL, which lands here. send_from_directory refuses paths that
escape UPLOAD_FOLDER, so <path:key> is traversal-safe.
"""

from flask import Blueprint, current_app, send_from_directory

uploads_bp = Blueprint('uploads_bp', __name__)


@uploads_bp.route('/uploads/<path:key>', methods=['GET'])
def serve_upload(key):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], key)
