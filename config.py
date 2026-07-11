import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Uploaded media (myth photo albums) ---
    # Files live on the LOCAL filesystem by default (uploads/ is gitignored).
    # STORAGE_BACKEND selects the app.storage implementation; a cloud backend
    # (e.g. S3-compatible) plugs in there without touching routes or models.
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    STORAGE_BACKEND = os.getenv('STORAGE_BACKEND', 'local')
    # Hard cap for a whole multipart request (Flask returns 413 beyond this).
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

    # The DB connection string (with credentials) must come from the
    # environment via .env, which is gitignored. Never hardcode credentials
    # here -- config.py is committed to source control.
    # Local dev example:  postgresql://postgres:a@localhost/IranianMythDb
    # Supabase (Session pooler):
    #   postgresql://postgres.<ref>:<password>@aws-1-<region>.pooler.supabase.com:5432/postgres
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):  # Inherit from Config
    DEBUG = True


class ProductionConfig(Config):  # Inherit from Config
    DEBUG = False


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
