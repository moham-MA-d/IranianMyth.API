from app.__init__ import create_app
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    


