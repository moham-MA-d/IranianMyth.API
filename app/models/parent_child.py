from app.extensions import db 


class ParentChild(db.Model):
    __tablename__ = 'parent_child'

    id = db.Column(db.String(10), primary_key=True, nullable=False)
    parent_id = db.Column(db.String(10), db.ForeignKey('myths.id'), nullable=False)
    child_id = db.Column(db.String(10), db.ForeignKey('myths.id'), nullable=False)
    relation_type = db.Column(db.String(50), nullable=False)  # e.g., biological, adoptive
    color = db.Column(db.String(20), nullable=True)  # Visualization color

    # Relationships
    parent = db.relationship("Myth", foreign_keys=[parent_id], backref="children")
    child = db.relationship("Myth", foreign_keys=[child_id], backref="parents")

    def __repr__(self):
        return f"<ParentChild Parent:{self.parent_id} Child:{self.child_id}>"
