# War Crimes and Chill Discord Bot

## Setup Instructions

1. Ensure all files are in the same directory on your VM.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Install FFmpeg on your system (required for audio playback):
   - On Ubuntu or Debian: `sudo apt-get install ffmpeg`
   - On macOS with Homebrew: `brew install ffmpeg`
   - On Windows: Download from https://ffmpeg.org/download.html and add to PATH
4. Set up your `.env` file with the following variables:
   - DISCORD_TOKEN
   - DATABASE_URL
   - OPENAI_API_KEY
   - GOOGLE_CALENDAR_CREDENTIALS_FILE
5. Place your `credentials.json` file for Google Calendar API in the same directory.
6. Run the bot:
   ```
   python bot.py
   ```

## Available Commands

### Server Setup
- `!setupserver`: Initializes the server layout (Task Master only)

### Voice Channels
- `!create_voice <channel_name>`: Creates a temporary voice channel

### Music
- `!play <url>`: Plays audio from the given URL (YouTube, Spotify, etc.)
- `!stop`: Stops the currently playing audio

### Custom Roles
- `!custom_role create <role_name> <color_hex>`: Creates a custom role
- `!custom_role delete <role_name>`: Deletes a custom role
- `!custom_role assign <role_name> <@member>`: Assigns a custom role to a member
- `!custom_role remove <role_name> <@member>`: Removes a custom role from a member

### Chain of Command
- `!coc set <position> <@member>`: Sets a member's position in the chain of command
- `!coc view`: Displays the current chain of command

### Meme Warfare
- `!meme submit <title>`: Submits a meme (attach an image)
- `!meme vote <meme_id>`: Votes for a meme
- `!meme leaderboard`: Displays the meme leaderboard

### PT Scores
- `!pt_score @member <pushups> <situps> <run_time>`: Updates a member's PT score
- `!pt_score @member`: Displays a member's PT score

### Training Management
- `!training schedule <name> <date> <description>`: Schedules a training event
- `!training complete <training_id>`: Marks a training as completed
- `!training list`: Lists all scheduled trainings

### Inventory Management
- `!inventory add <item_name> <quantity>`: Adds items to the inventory
- `!inventory remove <item_name> <quantity>`: Removes items from the inventory
- `!inventory list`: Lists all items in the inventory

### Attendance Management
- `!attendance mark <@member> <status>`: Marks a member's attendance
- `!attendance report <start_date> <end_date>`: Generates an attendance report

### Counseling
- `!counseling start <@member>`: Starts a counseling session
- `!endcounseling`: Ends the current counseling session

### Leaderboards
- `!leaderboard <board_type>`: Displays a leaderboard (overall, fitness, or gaming)

### Server Customization
- `!customize theme <banner_url> <icon_url> <primary_color>`: Updates server theme
- `!customize welcome <welcome_message>`: Sets the welcome message
- `!customize rules <rules_text>`: Updates server rules

### Calendar Integration
- `!calendar events`: Lists upcoming events from the Google Calendar

### AI Chat
- `!ask <question>`: Asks a question to the AI assistant

## Role Hierarchy

1. Task Master: Full access to all commands and server management
2. NCOs: Access to sensitive information and management commands
3. Regular Members: Access to general commands and participation features

## Bot Permissions

Ensure the bot has the following permissions:
- Manage Channels
- Manage Roles
- Read/Send Messages
- Manage Messages
- Embed Links
- Attach Files
- Read Message History
- Connect to Voice Channels
- Speak in Voice Channels

## Troubleshooting

If you encounter any issues:
1. Check the console for error messages
2. Ensure all environment variables are correctly set
3. Verify the bot has the necessary permissions in Discord
4. Check your internet connection and the status of the Discord API

For further assistance, contact the bot developer.

## Security Notes

- Keep your `.env` file and `credentials.json` secure and never share them publicly.
- Regularly update the bot and its dependencies to ensure security.
- Monitor the bot's activities and review logs periodically.

## Disclaimer

This bot is for entertainment and organizational purposes within a Discord server. Users are responsible for ensuring all activities comply with Discord's Terms of Service and Community Guidelines.