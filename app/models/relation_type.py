from app.extensions import db 

#Optional - A reference table to standardize relationship types.
class RelationType(db.Model):
    __tablename__ = 'relation_types'
    
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)  # e.g., marriage, friendship
    color = db.Column(db.String(20), nullable=True)  # Default color for visualization

    def __repr__(self):
        return f"<RelationType {self.id}-{self.name}>"