# X-Bot (Twitter Bot)

An automated Twitter bot that posts AI-generated tweets using Groq LLM API. The bot runs as a systemd service and posts tweets at configurable intervals.

## Features

- Twitter API integration using Tweepy
- AI-powered tweet generation using Groq LLM
- Automated posting via systemd timer service
- Configurable logging system
- Environment-based configuration
- Robust error handling and validation
- Type hints and documentation

## Prerequisites

- Python 3.8+
- Twitter Developer Account with API credentials
- Groq API key
- Linux system with systemd

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aman-Shitta/x-bot
cd x-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install tweepy python-dotenv groq
```

4. Create `.env` file in project root (get keys here: https://developer.x.com/):
```env
API_KEY=your_twitter_api_key
API_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_secret
BEARER_TOKEN=your_bearer_token
GROQ_API_KEY=your_groq_api_key
```

## Project Structure

```
x-bot/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── bot.py           # Twitter bot implementation
│   ├── config.py        # Configuration classes
│   ├── logging_config.py # Logging setup
│   ├── tweet_generator.py # AI tweet generation
│   ├── bot.service      # Systemd service file
│   ├── bot.timer        # Systemd timer file
│   └── helper.py        # Utility functions
├── tests/
├── .env
├── requirements.txt
└── README.md
```

## Usage

### Manual Run
```bash
cd src
python main.py
```

### Automated Service Setup
1. Set up systemd service:
```bash
mkdir -p ~/.config/systemd/user/
cp src/bot.service ~/.config/systemd/user/
cp src/bot.timer ~/.config/systemd/user/
```

2. Start the service:
```bash
systemctl --user daemon-reload
systemctl --user enable bot.timer
systemctl --user start bot.timer
```

3. Monitor logs:
```bash
tail -f ~/Projects/x-bot/twitterbot.log
```

## Configuration

### Environment Variables
Required variables in `.env`:
- `API_KEY`: Twitter API Key
- `API_SECRET`: Twitter API Secret
- `ACCESS_TOKEN`: Twitter Access Token
- `ACCESS_SECRET`: Twitter Access Secret
- `BEARER_TOKEN`: Twitter Bearer Token
- `GROQ_API_KEY`: Groq API Key

### AI Configuration
Modify `AIConfig` in `config.py`:
```python
AIConfig(
    prompt_template="Generate a tweet about {topic} in a {tone} tone",
    temperature=0.7,
    max_tokens=255,
    topics=["technology", "programming"],
    tone="professional"
)
```

### Service Configuration
Default timer interval is 30 minutes. To modify:
1. Edit `bot.timer`:
```ini
[Timer]
OnUnitActiveSec=30min
```
2. Reload service:
```bash
systemctl --user daemon-reload
systemctl --user restart bot.timer
```

## Logging

Logs are written to `twitterbot.log` with these levels:
- DEBUG: Detailed debugging information
- INFO: General operational information
- WARNING: Minor issues that don't affect core functionality
- ERROR: Serious issues that need attention

## License

MIT License - see LICENSE file for details

## Author

- Aman Shitta (amanshitta [at] gmail.com)

## Acknowledgments

- Tweepy library for Twitter API integration
- Groq AI for LLM capabilities (https://console.groq.com)
- Systemd for service management