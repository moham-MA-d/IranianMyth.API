from app.extensions import db 
    
class MythPhoto(db.Model):
    __tablename__ = 'myth_photos'
    
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    myth_id = db.Column(db.String(10), db.ForeignKey('myths.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)