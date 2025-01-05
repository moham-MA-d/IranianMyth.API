from app.extensions import db 

class Relationship(db.Model):
    __tablename__ = 'relationships'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    myth1_id = db.Column(db.String(10), db.ForeignKey('myths.id'), nullable=False)
    myth2_id = db.Column(db.String(10), db.ForeignKey('myths.id'), nullable=False)
    relation_type = db.Column(db.String(50), nullable=False)  # e.g., marriage, affair
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    relation_status = db.Column(db.String(20), nullable=True)  # e.g., active, ended
    description = db.Column(db.Text, nullable=True)
    points = db.Column(db.JSON, nullable=True)  # New field for link coordinates
    from_spot = db.Column(db.String(10), nullable=True, default="Bottom")  # e.g., "Top", "Left"
    to_spot = db.Column(db.String(10), nullable=True, default="Top")  # e.g., "Bottom", "Right"
    # Relationships
    myth1 = db.relationship("Myth", foreign_keys=[myth1_id], backref="relationships1")
    myth2 = db.relationship("Myth", foreign_keys=[myth2_id], backref="relationships2")

    def __repr__(self):
        return f"<Relationship {self.myth1_id}-{self.relation_type}-{self.myth2_id}>"