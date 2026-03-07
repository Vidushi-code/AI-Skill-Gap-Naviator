import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Keys
    CEREBRAS_API_KEY: str = os.environ.get("CEREBRAS_API_KEY", "")
    
    # AI Model Configuration
    AI_MODEL: str = "gpt-oss-120b"
    AI_TEMPERATURE: float = 0.7  # Higher temperature for more varied responses
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".doc", ".docx", ".txt"}
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "null",  # For file:// protocol
    ]
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.CEREBRAS_API_KEY:
            raise ValueError("CEREBRAS_API_KEY not found in environment variables")
        return True

# Create a settings instance
settings = Settings()
