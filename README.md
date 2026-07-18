# DiscordWeatherBot

A small Python script that posts current weather and a short multi-day forecast to a Discord channel using an OpenWeatherMap API key and a Discord webhook. It's designed to be run on a schedule (daily) and is configurable by environment variables.

## Features
- Fetches current weather for a configured city (OpenWeatherMap current weather API).
- Fetches a short multi-day forecast (OpenWeatherMap 5-day / 3-hour forecast).
- Posts a formatted message to a Discord webhook.
- Minimal dependencies: requests and schedule (schedule is included if you want to run the script as a long-running process).

## Stack
- Language: Python (single-file script)
- Runtime: CPython 3.8+
- Notable libraries: requests, schedule

## Repository layout
```
README.md            - this file (replaced/expanded)
main.py              - bot script: fetches weather + forecast, sends Discord webhook
requirements.txt     - Python dependencies (requests, schedule)
```

How it fits together:
- main.py contains everything: get_weather() (current weather), get_forecast() (multi-day forecast), send_discord_message() and send_daily_weather() which combines both and posts to your webhook. Environment variables supply the OpenWeatherMap API key and Discord webhook URL.

## Quick start (run locally)
1. Clone the repo:
   git clone https://github.com/Bobydong/DiscordWeatherBot.git
   cd DiscordWeatherBot

2. Create and activate a virtual environment, then install dependencies:
   python -m venv venv
   # macOS / Linux
   source venv/bin/activate
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1

   pip install -r requirements.txt

3. Set environment variables (examples):
   # Linux / macOS
   export API_KEY="your_openweathermap_api_key"
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
   export CITY="Livingston, NJ, US"        # optional — default in script
   export UNITS="imperial"                # optional — default in script

   # Windows PowerShell
   $env:API_KEY = "your_openweathermap_api_key"
   $env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
   $env:CITY = "Livingston, NJ, US"

4. Run:
   python main.py

When the script runs it will print status messages to stdout and attempt to send one Discord message using the configured webhook.

## Running daily (scheduling)
Option A — Cron (Linux/macOS)
- Add a cronjob to run main.py once a day (example: 07:00 local time):
  0 7 * * * /path/to/DiscordWeatherBot/venv/bin/python /path/to/DiscordWeatherBot/main.py >> /path/to/DiscordWeatherBot/weather.log 2>&1

Option B — Use schedule (long-running process)
- The repository includes `schedule` in requirements. To run as a long-running process that posts daily at 07:00 local time, add the following near the bottom of main.py (or run a small wrapper):

```python
import schedule
import time

schedule.every().day.at("07:00").do(send_daily_weather)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Note: schedule uses local machine time. For reliable production scheduling prefer system cron, systemd timers, or a cloud scheduler.

## Environment variables
- API_KEY (required) — OpenWeatherMap API key
- DISCORD_WEBHOOK_URL (required) — Discord incoming webhook URL
- CITY (optional) — city string used in OpenWeatherMap queries (default: "Livingston, NJ, US")
- UNITS (optional) — "imperial" or "metric" (default: "imperial")

## Troubleshooting
- Missing env vars: The script will try to call the APIs and will likely fail if API_KEY or DISCORD_WEBHOOK_URL are not set. Export them before running.
- OpenWeatherMap errors: If the API key is invalid or the city name is wrong, the OpenWeatherMap response will include an error message; check logs printed by the script.
- Discord webhooks: On success Discord returns HTTP 204 (no content). If you get a non-204, the script prints status and body — verify the webhook URL and permissions.
- Timezones: get_forecast() uses UTC timestamps to group forecast entries by date. If you need local-time grouping, convert timestamps to the target timezone before grouping.

## Suggested improvements
- Validate required environment variables at startup and exit with a clear message if missing.
- Add more robust error handling and retries for transient HTTP failures.
- Make CITY and the ping target (currently hard-coded `@brugen` in send_daily_weather) configurable.
- Add Dockerfile and a small systemd unit or GitHub Actions workflow if you want hosted deployments.

## Example message format
The bot posts Markdown-formatted content including condition, temperature, feels-like, humidity, wind speed and a multi-line forecast for the coming days. Example snippet:
**Weather Update for Livingston, NJ, US** ☀️
> **Condition:** clear sky
> **Temperature:** 77°F
> **Feels Like:** 76°F
> **Humidity:** 50%
> **Wind Speed:** 6 mph

**📆 Today's Forecast**
>**07:00 AM** - clear sky, 73°F
>**10:00 AM** - few clouds, 78°F

## Contributing
Small single-file project — open a PR with improvements (better error handling, configuration, tests, packaging) or open an issue describing features you'd like.

## License
Add your preferred license here (MIT, Apache-2.0, etc.) — none included in this repo currently.
