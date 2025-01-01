from app.extensions import db 


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    imageProfile = db.Column(db.String(100), nullable=True)
    imageBg = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
  
        
    def __repr__(self):
        return f"<Category {self.title}>"