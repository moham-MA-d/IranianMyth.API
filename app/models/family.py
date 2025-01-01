from app.extensions import db 


class Family(db.Model):
    __tablename__ = 'families'
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    imageProfile = db.Column(db.String(100), nullable=True)
    imageBg = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
  
        
    def __repr__(self):
        return f"<Family {self.title}>"