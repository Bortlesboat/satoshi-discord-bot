import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_URL = os.getenv("API_URL", "https://bitcoinsapi.com")
API_KEY = os.getenv("API_KEY", "")
