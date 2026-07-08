"""Myth photo album endpoints (admin authoring + public listing).

Album invariant, maintained by every mutation here:
  * photos of a myth are ordered by sort_order (0..n-1, no holes);
  * the MAIN photo is the one at sort_order 0 and the only is_main=True;
  * Myth.imageProfile always mirrors the main photo's url (or None when the
    album is empty) — /roots' "image" and the graph cards need no album logic.

Files themselves go through app.storage (local disk by default, cloud-ready);
every mutation returns the myth's full ordered album so clients never refetch.
"""

from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Myth, MythPhoto
from app.storage import (allowed_extension, get_storage, key_for_url,
                         make_photo_key)

myth_photos_bp = Blueprint('myth_photos_bp', __name__)


def _ordered_photos(myth_id):
    return (MythPhoto.query
            .filter_by(myth_id=myth_id)
            .order_by(MythPhoto.sort_order)
            .all())


def _renumber(photos, myth):
    """Re-apply the album invariant over `photos` (already in desired order)."""
    for i, p in enumerate(photos):
        p.sort_order = i
        p.is_main = i == 0
    myth.imageProfile = photos[0].url if photos else None


def _serialize(photos):
    return [p.to_dict() for p in photos]


@myth_photos_bp.route('/byMyth/<string:myth_id>', methods=['GET'])
def get_photos_for_myth(myth_id):
    if not Myth.query.get(myth_id):
        return jsonify({"isSuccess": False, "message": "Myth not found"}), 404
    return jsonify(_serialize(_ordered_photos(myth_id))), 200


@myth_photos_bp.route('/upload/<string:myth_id>', methods=['POST'])
def upload_photos(myth_id):
    try:
        myth = Myth.query.get(myth_id)
        if not myth:
            return jsonify({"isSuccess": False, "message": "Myth not found"}), 404

        files = request.files.getlist('files')
        if not files:
            return jsonify({"isSuccess": False, "message": "هیچ فایلی ارسال نشده است"}), 400

        # Validate the WHOLE batch before touching disk or DB: one bad file
        # rejects everything, so a multi-upload is all-or-nothing.
        exts = []
        for f in files:
            ext = allowed_extension(f.filename)
            if not ext or not (f.mimetype or '').startswith('image/'):
                return jsonify({
                    "isSuccess": False,
                    "message": f"فایل «{f.filename}» تصویر مجاز نیست (png/jpg/jpeg/webp/gif)",
                }), 400
            exts.append(ext)

        storage = get_storage()
        saved_keys = []
        try:
            new_photos = []
            for f, ext in zip(files, exts):
                key = make_photo_key(myth_id, ext)
                url = storage.save(f, key)
                saved_keys.append(key)
                title = (f.filename or '')[:100] or None  # column is String(100)
                new_photos.append(MythPhoto(myth_id=myth_id, url=url, title=title))

            # Newest first: the LAST file of the batch ends up main (order 0).
            ordered = list(reversed(new_photos)) + _ordered_photos(myth_id)
            for p in new_photos:
                db.session.add(p)
            _renumber(ordered, myth)
            db.session.commit()
        except Exception:
            # DB failed after files hit the disk — best-effort cleanup so the
            # storage doesn't accumulate orphans, then re-raise to the 500 path.
            db.session.rollback()
            for key in saved_keys:
                storage.delete(key)
            raise

        return jsonify({
            "isSuccess": True,
            "message": "تصاویر با موفقیت بارگذاری شد",
            "photos": _serialize(ordered),
        }), 200
    except Exception as e:
        return jsonify({"isSuccess": False, "message": f"An error occurred: {str(e)}"}), 500


@myth_photos_bp.route('/star/<string:photo_id>', methods=['PUT'])
def star_photo(photo_id):
    try:
        photo = MythPhoto.query.get(photo_id)
        if not photo:
            return jsonify({"isSuccess": False, "message": "Photo not found"}), 404
        myth = Myth.query.get(photo.myth_id)
        if not myth:
            return jsonify({"isSuccess": False, "message": "Myth not found"}), 404

        # Move the starred photo to the front; everything else keeps its
        # relative order.
        ordered = [p for p in _ordered_photos(photo.myth_id) if p.id != photo.id]
        ordered.insert(0, photo)
        _renumber(ordered, myth)
        db.session.commit()

        return jsonify({
            "isSuccess": True,
            "message": "تصویر اصلی تغییر کرد",
            "photos": _serialize(ordered),
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"isSuccess": False, "message": f"An error occurred: {str(e)}"}), 500


@myth_photos_bp.route('/<string:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    try:
        photo = MythPhoto.query.get(photo_id)
        if not photo:
            return jsonify({"isSuccess": False, "message": "Photo not found"}), 404
        myth = Myth.query.get(photo.myth_id)
        if not myth:
            return jsonify({"isSuccess": False, "message": "Myth not found"}), 404

        url = photo.url
        db.session.delete(photo)
        # Renumber survivors; if the main photo was deleted the next one is
        # promoted (or imageProfile clears when the album empties).
        ordered = [p for p in _ordered_photos(photo.myth_id) if p.id != photo.id]
        _renumber(ordered, myth)
        db.session.commit()

        # Remove the file only after the DB row is gone, and only for files we
        # store locally (external/cloud urls have no local key).
        key = key_for_url(url)
        if key:
            get_storage().delete(key)

        return jsonify({
            "isSuccess": True,
            "message": "تصویر حذف شد",
            "photos": _serialize(ordered),
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"isSuccess": False, "message": f"An error occurred: {str(e)}"}), 500
