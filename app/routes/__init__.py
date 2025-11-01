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
from .category_routes import category_bp  
from .family_routes import family_bp 
from .relation_type_routes import relation_type_bp  # New import

def register_routes(app):
    app.register_blueprint(root_bp, url_prefix='/roots')
    app.register_blueprint(myth_bp, url_prefix='/myths')
    app.register_blueprint(era_bp, url_prefix='/eras')
    app.register_blueprint(myth_photos_bp, url_prefix='/mythPhotos')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(family_bp, url_prefix='/families')
    app.register_blueprint(relation_type_bp, url_prefix='/relationTypes')  # New registration


   
