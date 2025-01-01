import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):  # Inherit from Config
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://prod_user:prod_password@localhost/prod_db')
    DEBUG = True

class ProductionConfig(Config):  # Inherit from Config
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgres://prod_user:prod_password@localhost/prod_db')
    DEBUG = False

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
