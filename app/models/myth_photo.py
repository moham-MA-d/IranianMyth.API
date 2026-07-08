import uuid
from datetime import datetime, timezone

from app.extensions import db


class MythPhoto(db.Model):
    """One image in a myth's photo album.

    Invariant (kept by the /mythPhotos routes): the MAIN photo is always the
    one with is_main=True AND sort_order=0, and Myth.imageProfile mirrors its
    url — so /roots' "image" field and the graph node cards stay in sync
    without knowing about albums.

    NOTE: adding columns to the live Postgres table needs a one-time manual
    migration — db.create_all() will NOT alter an existing table. See
    scripts/migrate_myth_photos.sql.
    """
    __tablename__ = 'myth_photos'

    id = db.Column(db.String(36), primary_key=True, nullable=False,
                   default=lambda: uuid.uuid4().hex)
    myth_id = db.Column(db.String(10), db.ForeignKey('myths.id'), nullable=False)
    # Relative path for locally-stored files ("uploads/myths/<id>/<name>.jpg")
    # or an absolute URL for external/cloud images.
    url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_main = db.Column(db.Boolean, nullable=False, default=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=lambda: datetime.now(timezone.utc))

    myth = db.relationship('Myth', backref='photos')

    def to_dict(self):
        return {
            'id': self.id,
            'myth_id': self.myth_id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'is_main': self.is_main,
            'sort_order': self.sort_order,
        }
