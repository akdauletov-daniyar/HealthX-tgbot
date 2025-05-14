 # Health-X Medical Assistant Bot

A Telegram bot that uses AI to provide preliminary medical assessments based on user-reported symptoms. The bot analyzes symptoms using AI model and provides possible diagnoses, treatment recommendations, and precautions.

⚠️ **Important Disclaimer**: This bot is not a replacement for professional medical advice. Always consult with healthcare professionals for proper medical diagnosis and treatment.

## Features

- Interactive symptom analysis
- AI-powered medical assessment
- Detailed response including:
  - Possible diagnoses
  - Treatment recommendations
  - Precautions
  - General medication information (where applicable)

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))
- OpenAI API Key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/akdauletov-daniyar/HealthX-tgbot.git
cd HealthX-tgbot
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python -m venv .venv
source .venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_telegram_bot_token_here` with your Telegram bot token and `your_openai_api_key_here` with your OpenAI API key.

## Running the Bot

1. Make sure your virtual environment is activated
2. Run the bot:
```bash
python __init__.py
```

The bot will start and begin listening for messages on Telegram.

## Usage

1. Start a chat with your bot on Telegram
2. Send the `/start` command to begin
3. Describe your symptoms in detail when prompted
4. Wait for the AI to analyze your symptoms and provide a response

## Environment Variables

The following environment variables must be set in the `.env` file:

- `BOT_TOKEN`: Your Telegram bot token (obtained from @BotFather)
- `OPENAI_API_KEY`: Your OpenAI API key

## Dependencies

- aiogram >= 3.0.0
- python-dotenv >= 0.19.0
- openai >= 1.0.0
- aiohttp >= 3.8.0

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them
- Regularly update your dependencies to patch security vulnerabilities

## Support

If you encounter any issues or have questions, please contact akdauletov.daniar@gmail.com
