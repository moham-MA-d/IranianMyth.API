# from .myth_routes import myth_bp
# from .era_routes import era_bp
# from .relationship_routes import relationship_bp
# from .parent_child_routes import parent_child_bp
# from .myth_photo_routes import myth_photo_bp

# def register_routes(app):
#     app.register_blueprint(myth_bp)
#     app.register_blueprint(era_bp)
#     app.register_blueprint(relationship_bp)
#     app.register_blueprint(parent_child_bp)
#     app.register_blueprint(myth_photo_bp)

from .root_routes import root_bp
from .myth_routes import myth_bp
from .era_routes import era_bp
from .myth_photo_routes import myth_photos_bp

def register_routes(app):
    app.register_blueprint(root_bp, url_prefix='/roots')
    app.register_blueprint(myth_bp, url_prefix='/myths')
    app.register_blueprint(era_bp, url_prefix='/eras')
    app.register_blueprint(myth_photos_bp, url_prefix='/mythPhotos')
   
