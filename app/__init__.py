from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate
from app.static.seed_data import seed_data  # Import the seed function
from app.models import Era
from flask_migrate import upgrade
import os
from config import config_map
import psycopg2
from psycopg2 import sql, OperationalError


def create_database_if_not_exists(database_url):
    """Create the PostgreSQL database if it doesn't exist."""
    from urllib.parse import urlparse
    try:
        # Parse the database URL
        url = urlparse(database_url)
        db_name = url.path[1:]  # Remove the leading "/"
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port or "5432"

        # Connect to the default database (postgres)
        print(f"Connecting to PostgreSQL server at {host}:{port} with user '{user}'...")
        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("Connection to PostgreSQL successful!")

        # Check if the database exists
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name]
        )
        exists = cursor.fetchone()

        # Create the database if it doesn't exist
        if not exists:
            print(f"Database '{db_name}' does not exist. Creating it...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()
    except OperationalError as e:
        print(f"Error: Could not connect to PostgreSQL. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    #CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}}, allow_headers=["Content-Type", "Authorization"])

    # Configurations
    # Dynamically load the configuration based on the FLASK_CONFIG environment variable
    config_name = os.getenv('FLASK_CONFIG')

    # Ensure the FLASK_CONFIG environment variable is set
    if not config_name:
      raise RuntimeError("The FLASK_CONFIG environment variable is not set. Please set it to 'development', 'production', or another valid environment.")

    # Ensure the configuration name is valid
    if config_name not in config_map:
      raise ValueError(f"Invalid FLASK_CONFIG value: '{config_name}'. Valid options are: {', '.join(config_map.keys())}")

    # Load the corresponding configuration class
    app.config.from_object(config_map[config_name])  
    
    
    # Ensure the database exists
    database_url = app.config["SQLALCHEMY_DATABASE_URI"]
    create_database_if_not_exists(database_url)
    
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)


    #Create database tables
    with app.app_context():
      db.create_all()
      #upgrade()  # Automatically apply migrations on app startup
       
      if db.session.query(Era).count() == 0:
        seed_data()
      
    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app
