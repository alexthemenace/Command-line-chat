# Instagram Command Line Chat 📱

A powerful command-line interface for Instagram Direct Messages. Send and receive Instagram DMs directly from your terminal with a clean, intuitive interface.

## Features

- 🔐 **Secure Authentication** - Login once and save session for future use
- 💬 **Full DM Support** - Send and receive direct messages
- 📋 **Conversation List** - View all your Instagram conversations
- 🔍 **User Search** - Find Instagram users to message
- 🎨 **Colored Output** - Beautiful terminal interface with colors
- 💾 **Session Management** - Automatic session saving and loading
- 🛡️ **Privacy Focused** - Credentials stored securely locally

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alexthemenace/Command-line-chat.git
   cd Command-line-chat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup wizard:**
   ```bash
   python instagram_chat.py setup
   ```

## Quick Start

### 1. Initial Setup
Run the setup wizard to configure your Instagram credentials:
```bash
python instagram_chat.py setup
```

### 2. View Your Conversations
List all your Instagram DM conversations:
```bash
python instagram_chat.py conversations
```

### 3. Send a Message
Send a direct message to any Instagram user:
```bash
python instagram_chat.py send username "Hello from the command line!"
```

### 4. Chat Interactively
Open a conversation for real-time chatting:
```bash
python instagram_chat.py chat 1
```

## Commands

### Authentication
- `setup` - First-time configuration wizard
- `login` - Login to Instagram manually
- `status` - Check authentication status

### Messaging
- `conversations` - List all DM conversations
- `chat <number>` - Open interactive chat with conversation
- `send <username> <message>` - Send a message to a user
- `search <query>` - Search for Instagram users

## Usage Examples

### Setup and First Login
```bash
# Run the setup wizard
python instagram_chat.py setup

# Or login manually
python instagram_chat.py login -u your_username
```

### Viewing and Managing Conversations
```bash
# List all conversations
python instagram_chat.py conversations

# Open conversation #1 for chatting
python instagram_chat.py chat 1

# View last 20 messages in conversation #2
python instagram_chat.py chat 2 --limit 20
```

### Sending Messages
```bash
# Send a quick message
python instagram_chat.py send johndoe "Hey, how are you?"

# Send a longer message
python instagram_chat.py send johndoe "This is a longer message with multiple words"
```

### Finding Users
```bash
# Search for users
python instagram_chat.py search "john"
```

## Configuration

The app uses a `.env` file for configuration. Create one with:

```env
# Required
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# Optional
MAX_MESSAGES_DISPLAY=10
POLLING_INTERVAL=5
```

**Security Note:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Features in Detail

### 🔐 Secure Session Management
- Sessions are saved locally and encrypted
- No need to login every time you use the app
- Automatic session validation and renewal

### 💬 Interactive Chat Mode
- Real-time conversation interface
- Color-coded messages (you vs. others)
- Type and send messages instantly
- Clean, readable message history

### 🎨 Beautiful Terminal Interface
- Colorized output for better readability
- Emojis and icons for visual clarity
- Clean formatting and organization
- Cross-platform color support

## Troubleshooting

### Common Issues

**Login Failed:**
- Verify your username and password
- Check if Instagram requires verification (check your phone/email)
- Try logging in from Instagram app first

**"User not found" Error:**
- Make sure the username is spelled correctly
- The user might have a private account
- Try searching for the user first

**Session Expired:**
- Run `python instagram_chat.py login` to refresh
- Delete the session file and login again

### Getting Help
```bash
# Get general help
python instagram_chat.py --help

# Get help for specific commands
python instagram_chat.py send --help
python instagram_chat.py chat --help
```

## Requirements

- Python 3.7+
- Instagram account
- Required packages (see `requirements.txt`)

## Security & Privacy

- All credentials are stored locally only
- Session files are encrypted
- No data is sent to third parties
- Uses official Instagram API methods
- Respects Instagram's rate limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for educational and personal use only. Please respect Instagram's Terms of Service and use responsibly. The developers are not responsible for any misuse of this tool.
