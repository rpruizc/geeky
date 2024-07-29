import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE = os.path.join(os.getcwd(), 'website_analyzer.db')
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")