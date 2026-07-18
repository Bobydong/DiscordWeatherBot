# DiscordWeatherBot

A small Python script that posts current weather and a short multi-day forecast to a Discord channel using an OpenWeatherMap API key and a Discord webhook. It's designed to be run on a schedule (daily) and is configurable by environment variables.

## Features
- Fetches current weather for a configured city (OpenWeatherMap current weather API).
- Fetches a short multi-day forecast (OpenWeatherMap 5-day / 3-hour forecast).
- Posts a formatted message to a Discord webhook.
- Minimal dependencies: requests and schedule (schedule is included if you want to run the script as a long-running process).

## Stack
- Language: Python 3.12
- Notable libraries: requests, schedule

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

