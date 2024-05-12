from dotenv import load_dotenv
from pydantic import EmailStr
import os

load_dotenv()

email: EmailStr = os.getenv("EMAIL")
key = os.getenv("PASSWORD")