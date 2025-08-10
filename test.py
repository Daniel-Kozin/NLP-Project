import os
from dotenv import load_dotenv

# Get the API KEY
load_dotenv()  # Load variables from .env file
api_key = os.getenv("API_KEY")
print(api_key)