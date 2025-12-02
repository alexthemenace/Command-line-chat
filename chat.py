"""Chat functionality for Instagram CLI Chat."""
from datetime import datetime
import click
from colorama import Fore, Style, init
from instagrapi.exceptions import ClientError
from config import Config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class InstagramChat:
    """Handle Instagram direct messaging functionality."""
    
    def __init__(self, client):
        self.client = client
        self.current_user = None
        self._get_current_user()
    
    def _get_current_user(self):
        """Get current user information."""
        try:
            self.current_user = self.client.account_info()
        except Exception as e:
            click.echo(f"❌ Failed to get user info: {e}")
    
    def list_conversations(self):
        """List all direct message conversations."""
        try:
            click.echo(f"\n{Fore.CYAN}📱 Your Instagram Direct Messages:{Style.RESET_ALL}")
            click.echo("=" * 50)
            
            threads = self.client.direct_threads()
            
            if not threads:
                click.echo(f"{Fore.YELLOW}No conversations found{Style.RESET_ALL}")
                return []
            
            conversations = []
            for i, thread in enumerate(threads[:20], 1):  # Limit to 20 conversations
                users = thread.users
                if users:
                    # Handle group chats vs individual chats
                    if len(users) > 1:
                        names = [user.username for user in users]
                        display_name = f"Group: {', '.join(names[:3])}"
                        if len(names) > 3:
                            display_name += f" (+{len(names)-3} more)"
                    else:
                        display_name = users[0].username
                    
                    # Get last message info
                    last_message = ""
                    timestamp = ""
                    if thread.messages:
                        last_msg = thread.messages[0]
                        if hasattr(last_msg, 'text') and last_msg.text:
                            last_message = last_msg.text[:50] + "..." if len(last_msg.text) > 50 else last_msg.text
                        elif hasattr(last_msg, 'media'):
                            last_message = "[Media]"
                        else:
                            last_message = "[Message]"
                        
                        if hasattr(last_msg, 'timestamp'):
                            timestamp = last_msg.timestamp.strftime("%m/%d %H:%M")
                    
                    click.echo(f"{Fore.GREEN}{i:2d}.{Style.RESET_ALL} {Fore.BLUE}{display_name:<20}{Style.RESET_ALL} "
                             f"{Fore.WHITE}{last_message:<30}{Style.RESET_ALL} {Fore.YELLOW}{timestamp}{Style.RESET_ALL}")
                    
                    conversations.append({
                        'index': i,
                        'thread_id': thread.id,
                        'display_name': display_name,
                        'users': users
                    })
            
            return conversations
            
        except Exception as e:
            click.echo(f"❌ Failed to list conversations: {e}")
            return []
    
    def get_messages(self, thread_id, limit=None):
        """Get messages from a specific conversation."""
        try:
            limit = limit or Config.MAX_MESSAGES_DISPLAY
            messages = self.client.direct_messages(thread_id, amount=limit)
            return messages
        except Exception as e:
            click.echo(f"❌ Failed to get messages: {e}")
            return []

    def fetch_messages(self, thread_id, limit=20):
        """Fetch messages and return a stable, simple list of dicts.

        The returned list items have keys: 'id', 'timestamp', 'user_id', 'text'.
        This normalizes the instagrapi message objects so polling logic can
        dedupe and print messages without depending on the library types.
        """
        try:
            messages = self.client.direct_messages(thread_id, amount=limit)
            results = []
            for m in messages:
                # Try to derive a stable id; fall back to timestamp+user
                msg_id = getattr(m, 'id', None) or getattr(m, 'pk', None)
                if not msg_id:
                    try:
                        msg_id = f"{m.timestamp.timestamp()}_{m.user_id}"
                    except Exception:
                        msg_id = str(id(m))

                # Timestamp to ISO string if available
                ts = None
                try:
                    ts = m.timestamp.isoformat() if getattr(m, 'timestamp', None) else None
                except Exception:
                    ts = None

                text = ''
                try:
                    if getattr(m, 'text', None):
                        text = m.text
                except Exception:
                    text = ''

                user_id = getattr(m, 'user_id', None)

                results.append({
                    'id': str(msg_id),
                    'timestamp': ts,
                    'user_id': user_id,
                    'text': text,
                })

            return results
        except Exception as e:
            click.echo(f"❌ Failed to fetch messages: {e}")
            return []
    
    def display_messages(self, thread_id, display_name, limit=None):
        """Display messages from a conversation."""
        try:
            messages = self.get_messages(thread_id, limit)
            
            if not messages:
                click.echo(f"{Fore.YELLOW}No messages found in this conversation{Style.RESET_ALL}")
                return
            
            click.echo(f"\n{Fore.CYAN}💬 Conversation with {display_name}:{Style.RESET_ALL}")
            click.echo("=" * 60)
            
            # Reverse to show oldest first
            for message in reversed(messages):
                try:
                    sender = message.user_id
                    is_me = sender == self.current_user.pk
                    
                    # Format timestamp
                    timestamp = message.timestamp.strftime("%H:%M")
                    
                    # Get message content
                    content = ""
                    if hasattr(message, 'text') and message.text:
                        content = message.text
                    elif hasattr(message, 'media'):
                        content = "[Media message]"
                    else:
                        content = "[Message]"
                    
                    # Color code based on sender
                    if is_me:
                        click.echo(f"{Fore.GREEN}[{timestamp}] You:{Style.RESET_ALL} {content}")
                    else:
                        click.echo(f"{Fore.BLUE}[{timestamp}] {display_name}:{Style.RESET_ALL} {content}")
                
                except Exception as e:
                    click.echo(f"⚠️  Error displaying message: {e}")
            
            click.echo("=" * 60)
            
        except Exception as e:
            click.echo(f"❌ Failed to display messages: {e}")
    
    def send_message(self, username_or_thread_id, message_text):
        """Send a direct message to a user or thread."""
        try:
            # If it's a thread ID (numeric), send to thread
            if str(username_or_thread_id).isdigit():
                thread_id = username_or_thread_id
                result = self.client.direct_send(message_text, [], thread_ids=[thread_id])
            else:
                # It's a username, find or create thread
                username = username_or_thread_id
                user_id = self.client.user_id_from_username(username)
                result = self.client.direct_send(message_text, [user_id])
            
            if result:
                click.echo(f"{Fore.GREEN}✅ Message sent successfully!{Style.RESET_ALL}")
                return True
            else:
                click.echo(f"{Fore.RED}❌ Failed to send message{Style.RESET_ALL}")
                return False
                
        except ClientError as e:
            if "User not found" in str(e):
                click.echo(f"{Fore.RED}❌ User '{username_or_thread_id}' not found{Style.RESET_ALL}")
            else:
                click.echo(f"{Fore.RED}❌ Failed to send message: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}❌ Failed to send message: {e}{Style.RESET_ALL}")
            return False
    
    def search_users(self, query):
        """Search for users by username."""
        try:
            users = self.client.search_users(query)
            if not users:
                click.echo(f"{Fore.YELLOW}No users found for '{query}'{Style.RESET_ALL}")
                return []
            
            click.echo(f"\n{Fore.CYAN}🔍 Search results for '{query}':{Style.RESET_ALL}")
            click.echo("-" * 40)
            
            for i, user in enumerate(users[:10], 1):  # Limit to 10 results
                full_name = user.full_name or "No name"
                click.echo(f"{Fore.GREEN}{i:2d}.{Style.RESET_ALL} {Fore.BLUE}@{user.username}{Style.RESET_ALL} - {full_name}")
            
            return users[:10]
            
        except Exception as e:
            click.echo(f"❌ Failed to search users: {e}")
            return []