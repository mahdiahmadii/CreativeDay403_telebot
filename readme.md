# Telegram Bot for Khalaqiat va Neshat Ceremony

This project is a Telegram bot designed for the Khalaqiat va Neshat ceremony at Yazd University. It features registration via QR code generation, voting, sending memes, and more.

## Features

- **User Menu:**
  - Send messages
  - View event schedule
  - Participate in AI quiz
  - View QR code for registration
  - View image gallery
  - Edit user information
  - Send memes
  - Participate in polls for faculty talk shows

- **Admin Menu:**
  - Ban/Unban users
  - See messages
  - View user list
  - View admin list
  - Promote/Unpromote users
  - Broadcast messages
  - Show chat

## Requirements

1. Make sure you have Python installed (preferably Python 3.6 or higher).
2. Create a Telegram bot and get its token from BotFather.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace the `api_token` in `app.py` or create a `.env` file with your bot's API token.

4. Ensure that the server running the bot can connect to the Telegram server (use VPN if necessary).

5. Run the bot:
   ```bash
   python app.py
   ```

## Files Overview

- **app.py**: Main code for the Telegram bot.
- **database.py**: Contains functions to communicate with the SQLite database.
- **QR_codegenerator.py**: Responsible for generating and detecting QR codes using user information.

## Contributing

This bot is developed by an enthusiast of creating Telegram bots using the Telebot library. Feel free to contribute to the code or suggest improvements!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


