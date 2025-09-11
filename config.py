"""Configuration management for Instagram CLI Chat."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the Instagram chat application."""
    
    # Instagram API settings
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    
    # Session file location
    SESSION_FILE = Path.home() / '.instagram_chat_session.json'
    
    # App settings
    MAX_MESSAGES_DISPLAY = int(os.getenv('MAX_MESSAGES_DISPLAY', '10'))
    POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', '5'))  # seconds
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.INSTAGRAM_USERNAME:
            raise ValueError("INSTAGRAM_USERNAME environment variable is required")
        if not cls.INSTAGRAM_PASSWORD:
            raise ValueError("INSTAGRAM_PASSWORD environment variable is required")
        
        return True