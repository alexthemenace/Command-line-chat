"""Authentication module for Instagram CLI Chat."""
import json
import sys
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, BadPassword, ChallengeRequired
from config import Config
import click

class InstagramAuth:
    """Handle Instagram authentication and session management."""
    
    def __init__(self):
        self.client = Client()
        self.session_file = Config.SESSION_FILE
        
    def load_session(self):
        """Load existing session if available."""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                self.client.set_settings(session_data)
                click.echo("📱 Loaded existing Instagram session")
                return True
            except Exception as e:
                click.echo(f"⚠️  Failed to load session: {e}")
                return False
        return False
    
    def save_session(self):
        """Save current session to file."""
        try:
            session_data = self.client.get_settings()
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            click.echo("💾 Session saved successfully")
        except Exception as e:
            click.echo(f"⚠️  Failed to save session: {e}")
    
    def login(self, username=None, password=None):
        """Login to Instagram with provided or configured credentials."""
        username = username or Config.INSTAGRAM_USERNAME
        password = password or Config.INSTAGRAM_PASSWORD
        
        if not username or not password:
            click.echo("❌ Username and password are required")
            return False
        
        try:
            click.echo(f"🔐 Logging into Instagram as {username}...")
            self.client.login(username, password)
            click.echo("✅ Successfully logged into Instagram!")
            self.save_session()
            return True
            
        except BadPassword:
            click.echo("❌ Invalid username or password")
            return False
        except ChallengeRequired as e:
            click.echo("⚠️  Instagram requires additional verification")
            click.echo("Please check your Instagram app for security verification")
            return False
        except Exception as e:
            click.echo(f"❌ Login failed: {e}")
            return False
    
    def verify_login(self):
        """Verify that the current session is valid."""
        try:
            user_info = self.client.account_info()
            click.echo(f"✅ Authenticated as: {user_info.username}")
            return True
        except LoginRequired:
            click.echo("❌ Login required")
            return False
        except Exception as e:
            click.echo(f"❌ Authentication verification failed: {e}")
            return False
    
    def authenticate(self):
        """Main authentication flow."""
        # Try loading existing session first
        if self.load_session():
            if self.verify_login():
                return True
            else:
                click.echo("🔄 Session expired, logging in again...")
        
        # If no valid session, perform login
        return self.login()
    
    def get_client(self):
        """Get authenticated Instagram client."""
        return self.client