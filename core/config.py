import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'PersonaAnalyzer/1.0')
    
    # OpenAI
    # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    
    # App settings
    MAX_POSTS = 50
    MAX_COMMENTS = 50
    PERSONA_DIR = "./data/personas"
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.REDDIT_CLIENT_ID:
            missing.append('REDDIT_CLIENT_ID')
        if not cls.REDDIT_CLIENT_SECRET:
            missing.append('REDDIT_CLIENT_SECRET')
        if not cls.GROQ_API_KEY:
            missing.append('GROQ_API_KEY')
        
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
        
        return True

config = Config()