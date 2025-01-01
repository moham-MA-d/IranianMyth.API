import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

secret_key = os.getenv("FLASK_ENV")
database_url = os.getenv("FLASK_APP")

print(secret_key)
print(database_url)
