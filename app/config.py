from dotenv import load_dotenv
import os

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_ENCRYPTION_KEY = os.getenv("SECRET_ENCRYPTION_KEY")