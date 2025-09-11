#!/usr/bin/env python3
"""
Example usage of Instagram CLI Chat
This file demonstrates how to use the Instagram command-line chat application.
"""

# Example .env file content (create this file with your actual credentials)
ENV_EXAMPLE = """
# Instagram CLI Chat Configuration
# Create a .env file with these settings and your actual credentials

INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Optional settings
MAX_MESSAGES_DISPLAY=10
POLLING_INTERVAL=5
"""

# Example usage scenarios
USAGE_EXAMPLES = """
Instagram CLI Chat - Usage Examples
===================================

1. FIRST TIME SETUP:
   python instagram_chat.py setup
   # This will guide you through the initial configuration

2. LOGIN TO INSTAGRAM:
   python instagram_chat.py login
   # Or with specific credentials:
   python instagram_chat.py login -u your_username

3. CHECK AUTHENTICATION STATUS:
   python instagram_chat.py status

4. LIST YOUR CONVERSATIONS:
   python instagram_chat.py conversations
   # Shows all your Instagram DM conversations with numbers

5. SEND A QUICK MESSAGE:
   python instagram_chat.py send johndoe "Hey, how are you?"
   python instagram_chat.py send username "Hello from the command line!"

6. INTERACTIVE CHAT MODE:
   python instagram_chat.py chat 1
   # Opens conversation #1 for real-time chatting
   # Type messages and press Enter to send
   # Type 'quit' to exit

7. VIEW CONVERSATION HISTORY:
   python instagram_chat.py chat 2 --limit 20
   # Shows last 20 messages from conversation #2

8. SEARCH FOR USERS:
   python instagram_chat.py search "john"
   # Finds Instagram users matching "john"

9. GET HELP:
   python instagram_chat.py --help
   python instagram_chat.py send --help
   python instagram_chat.py chat --help

WORKFLOW EXAMPLE:
================
1. python instagram_chat.py setup          # Initial setup
2. python instagram_chat.py conversations  # See your chats
3. python instagram_chat.py chat 1         # Open conversation #1
   > Hello there!                          # Type and send message
   > How are you doing?                    # Send another message
   > quit                                  # Exit chat mode
4. python instagram_chat.py send newuser "Hi from CLI!"  # Message new user

FEATURES:
=========
✅ Secure session management (login once, use everywhere)
✅ Colorized terminal output for better readability
✅ Interactive chat mode with real-time messaging
✅ User search and discovery
✅ Conversation history viewing
✅ Cross-platform compatibility
✅ Error handling and helpful messages
✅ Beautiful terminal interface with emojis

SECURITY NOTES:
==============
- Your credentials are stored locally in .env file
- Session data is saved securely on your machine
- No data is sent to third parties
- Always keep your .env file private and secure
"""

if __name__ == "__main__":
    print("Instagram CLI Chat - Example Usage")
    print("=" * 50)
    print("\n.env file example:")
    print(ENV_EXAMPLE)
    print("\nUsage examples:")
    print(USAGE_EXAMPLES)