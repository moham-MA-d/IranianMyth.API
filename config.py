import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

# $env:DATABASE_URL="postgresql://postgres.bgxhyccolytvimlynryr:h41pYQxPnIhF1eYp@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"