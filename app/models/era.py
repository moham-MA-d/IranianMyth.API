from app.extensions import db 

class Era(db.Model):
    __tablename__ = 'eras'
    
    id: int  = db.Column(db.String(10), primary_key=True, nullable=False)
    name: str = db.Column(db.String(100), nullable=False)
    oldName: str = db.Column(db.String(100), nullable=False)
    image: str = db.Column(db.String(300), nullable=True)
    color: str = db.Column(db.String(100), nullable=True)
    description: str = db.Column(db.Text, nullable=True)
    order: str = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f"<Era {self.name}>"
