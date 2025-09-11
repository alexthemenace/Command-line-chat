#!/usr/bin/env python3
"""
Instagram Command Line Chat
A simple CLI tool to send and receive Instagram direct messages.
"""

import sys
import click
from colorama import Fore, Style, init
from auth import InstagramAuth
from chat import InstagramChat
from config import Config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_banner():
    """Print application banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    📱 Instagram CLI Chat                     ║
║              Send and receive Instagram DMs from CLI         ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    click.echo(banner)

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Instagram Command Line Chat - Send and receive Instagram DMs from your terminal."""
    print_banner()

@cli.command()
@click.option('--username', '-u', help='Instagram username')
@click.option('--password', '-p', help='Instagram password')
def login(username, password):
    """Login to Instagram and save session."""
    auth = InstagramAuth()
    
    # Use provided credentials or prompt for them
    if not username:
        username = click.prompt('Instagram username')
    if not password:
        password = click.prompt('Instagram password', hide_input=True)
    
    if auth.login(username, password):
        click.echo(f"{Fore.GREEN}✅ Successfully logged in and session saved!{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}❌ Login failed{Style.RESET_ALL}")
        sys.exit(1)

@cli.command()
def conversations():
    """List all your direct message conversations."""
    auth = InstagramAuth()
    
    if not auth.authenticate():
        click.echo(f"{Fore.RED}❌ Authentication failed. Please run 'login' command first.{Style.RESET_ALL}")
        sys.exit(1)
    
    chat = InstagramChat(auth.get_client())
    conversations = chat.list_conversations()
    
    if conversations:
        click.echo(f"\n{Fore.GREEN}💡 Use 'chat <number>' to open a conversation{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}💡 Use 'send <username> <message>' to send a new message{Style.RESET_ALL}")

@cli.command(name='chat')
@click.argument('conversation_id', type=int)
@click.option('--limit', '-l', default=10, help='Number of messages to display')
def chat_cmd(conversation_id, limit):
    """View messages in a specific conversation. Use the number from 'conversations' command."""
    auth = InstagramAuth()
    
    if not auth.authenticate():
        click.echo(f"{Fore.RED}❌ Authentication failed. Please run 'login' command first.{Style.RESET_ALL}")
        sys.exit(1)
    
    chat = InstagramChat(auth.get_client())
    conversations = chat.list_conversations()
    
    # Find the conversation
    selected_conv = None
    for conv in conversations:
        if conv['index'] == conversation_id:
            selected_conv = conv
            break
    
    if not selected_conv:
        click.echo(f"{Fore.RED}❌ Conversation {conversation_id} not found{Style.RESET_ALL}")
        return
    
    chat.display_messages(
        selected_conv['thread_id'], 
        selected_conv['display_name'], 
        limit
    )
    
    # Interactive mode
    click.echo(f"\n{Fore.YELLOW}💬 Type your message and press Enter (or 'quit' to exit):{Style.RESET_ALL}")
    
    while True:
        try:
            message = click.prompt('>', prompt_suffix=' ', show_default=False)
            
            if message.lower() in ['quit', 'exit', 'q']:
                break
            
            if message.strip():
                if chat.send_message(selected_conv['thread_id'], message):
                    click.echo(f"{Fore.GREEN}[You]: {message}{Style.RESET_ALL}")
                    
        except (KeyboardInterrupt, EOFError):
            break
    
    click.echo(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")

@cli.command()
@click.argument('username')
@click.argument('message', nargs=-1, required=True)
def send(username, message):
    """Send a direct message to a user."""
    auth = InstagramAuth()
    
    if not auth.authenticate():
        click.echo(f"{Fore.RED}❌ Authentication failed. Please run 'login' command first.{Style.RESET_ALL}")
        sys.exit(1)
    
    chat = InstagramChat(auth.get_client())
    message_text = ' '.join(message)
    
    click.echo(f"📤 Sending message to @{username}: {message_text}")
    
    if chat.send_message(username, message_text):
        click.echo(f"{Fore.GREEN}✅ Message sent to @{username}!{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.RED}❌ Failed to send message to @{username}{Style.RESET_ALL}")

@cli.command()
@click.argument('query')
def search(query):
    """Search for Instagram users."""
    auth = InstagramAuth()
    
    if not auth.authenticate():
        click.echo(f"{Fore.RED}❌ Authentication failed. Please run 'login' command first.{Style.RESET_ALL}")
        sys.exit(1)
    
    chat = InstagramChat(auth.get_client())
    users = chat.search_users(query)
    
    if users:
        click.echo(f"\n{Fore.GREEN}💡 Use 'send <username> <message>' to send a message{Style.RESET_ALL}")

@cli.command()
def status():
    """Check authentication status."""
    auth = InstagramAuth()
    
    if auth.load_session() and auth.verify_login():
        user_info = auth.get_client().account_info()
        click.echo(f"{Fore.GREEN}✅ Authenticated as: @{user_info.username}{Style.RESET_ALL}")
        click.echo(f"   Full name: {user_info.full_name}")
        click.echo(f"   Followers: {user_info.follower_count}")
        click.echo(f"   Following: {user_info.following_count}")
    else:
        click.echo(f"{Fore.RED}❌ Not authenticated. Please run 'login' command.{Style.RESET_ALL}")

@cli.command()
def setup():
    """Setup wizard for first-time configuration."""
    click.echo(f"{Fore.CYAN}🚀 Instagram CLI Chat Setup Wizard{Style.RESET_ALL}")
    click.echo("=" * 40)
    
    # Check if .env file exists
    env_file = ".env"
    env_exists = False
    
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            env_exists = 'INSTAGRAM_USERNAME' in content
    except FileNotFoundError:
        pass
    
    if env_exists:
        click.echo(f"{Fore.YELLOW}⚠️  Configuration file already exists{Style.RESET_ALL}")
        if not click.confirm("Do you want to reconfigure?"):
            return
    
    click.echo(f"\n{Fore.BLUE}📝 Please enter your Instagram credentials:{Style.RESET_ALL}")
    username = click.prompt('Instagram username')
    password = click.prompt('Instagram password', hide_input=True)
    
    # Create .env file
    env_content = f"""# Instagram CLI Chat Configuration
INSTAGRAM_USERNAME={username}
INSTAGRAM_PASSWORD={password}

# Optional settings
MAX_MESSAGES_DISPLAY=10
POLLING_INTERVAL=5
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    click.echo(f"\n{Fore.GREEN}✅ Configuration saved to .env file{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}⚠️  Keep your .env file secure and don't share it!{Style.RESET_ALL}")
    
    # Test login
    click.echo(f"\n{Fore.BLUE}🔐 Testing login...{Style.RESET_ALL}")
    auth = InstagramAuth()
    if auth.login(username, password):
        click.echo(f"\n{Fore.GREEN}🎉 Setup completed successfully!{Style.RESET_ALL}")
        click.echo(f"\n{Fore.CYAN}Next steps:{Style.RESET_ALL}")
        click.echo("  • Run 'instagram-chat conversations' to see your chats")
        click.echo("  • Run 'instagram-chat send <username> <message>' to send a message")
        click.echo("  • Run 'instagram-chat --help' for more commands")
    else:
        click.echo(f"\n{Fore.RED}❌ Setup failed. Please check your credentials.{Style.RESET_ALL}")

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}👋 Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        click.echo(f"\n{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)