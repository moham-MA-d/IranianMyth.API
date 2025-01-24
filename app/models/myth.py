from app.extensions import db 


class Myth(db.Model):
    __tablename__ = 'myths'
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=True)
    pos = db.Column(db.String(20), nullable=True)
    imageProfile = db.Column(db.String(100), nullable=True)
    imageBg = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    importance = db.Column(db.String(10), nullable=True)
    khvarenah = db.Column(db.Boolean, default=False)
    shape = db.Column(db.String(20), nullable=True, default="box-large")
    description = db.Column(db.Text, nullable=True)
    era_id = db.Column(db.String(10), db.ForeignKey('eras.id'), nullable=False)
    family_id = db.Column(db.String(10), db.ForeignKey('families.id'), nullable=False)
    category_id = db.Column(db.String(10), db.ForeignKey('categories.id'), nullable=False)
    era = db.relationship('Era', backref='myths')
    family = db.relationship('Family', backref='myths')
    category = db.relationship('Category', backref='myths')

        
    def __repr__(self):
        return f"<Myth {self.name}>"