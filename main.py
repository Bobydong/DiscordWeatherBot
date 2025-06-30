import requests
import time
from datetime import datetime, timedelta
import os


print("Script started. Current local time is:", datetime.now().strftime("%H:%M")) #finds the enviornment's local time

API_KEY = os.getenv("API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CITY = "Livingston, NJ, US"
UNITS = "imperial"

def get_weather(city_name): #uses their 2.5 version bc that one is completely free to get the current weather
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    data = response.json()
    #error message
    if str(data.get('cod')) != "200":
        return("Error:", data.get('message'))
    #data assignment/fetching
    desc = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    emoji = "☀️" if "clear" in desc.lower() else "☁️" if "cloud" in desc.lower() else "🌧️"
    txt = f"**Weather Update for {city_name}** {emoji}\n\n"
    txt += f"> **Condition:** {desc}\n"
    txt += f"> **Temperature:** {temp}°F\n"
    txt += f"> **Feels Like:** {feels_like}°F\n"
    txt += f"> **Humidity:** {humidity}%\n"
    txt += f"> **Wind Speed:** {wind_speed} mph\n"

  #    txt = f"Hello! \nThe current temperature in {city_name}, is {temp}°F and feels like {feels_like}°F. There is currently {desc} with winds of {wind_speed}.\nThe humidity is {humidity}%"
    print(txt)
    return txt

def send_discord_message(webhook_url, message):
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
      print("Message sent to Discord successfully.")
    else:
      print("Failed to send message to Discord. Status code:", response.status_code, response.text)

def send_daily_weather():
    current = get_weather(CITY)
    forecast = get_forecast(CITY)
    message = f"@brugen \nGood Morning!! \n{current}\n\n{forecast}"
    send_discord_message(DISCORD_WEBHOOK_URL, message)
    print("sent")

def get_forecast(city_name):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    data = response.json()
    if str(data.get('cod')) != "200":
        return("Error:", data.get('message'))
    forecast_list = data["list"]
    now = datetime.utcnow()
    #7 day forecast
    today = now.date() #day 1
    tomorrow = today + timedelta(days=1) #day 2
    day3 = today + timedelta(days=2) #day 3
    day4 = today + timedelta(days=3) #day 4
    day5 = today + timedelta(days=4) #day 5
    day6 = today + timedelta(days=5) #day 6
    day7 = today + timedelta(days=6) #day 7


    today_forecasts = []
    tomorrow_forecasts = []
    day3_forecasts = []
    day4_forecasts = []
    day5_forecasts = []

############
    for entry in forecast_list:
      timestamp = datetime.utcfromtimestamp(entry["dt"])
      date = timestamp.date()
      time_str = timestamp.strftime("%I:%M %p")
      desc = entry["weather"][0]["description"]
      temp = entry["main"]["temp"]
      feels_like = entry["main"]["feels_like"]
      temp_min = entry["main"]["temp_min"]
      temp_max = entry["main"]["temp_max"]

      line = f">**{time_str}** - {desc}, {temp}°F"
      if date == today:
        today_forecasts.append(line)
      elif date == tomorrow and len(tomorrow_forecasts) < 7: #7 because it seems like there are only 7 data points per day
        tomorrow_forecasts.append(line)
      elif date == day3 and len(day3_forecasts) < 7:
        day3_forecasts.append(line)
      elif date == day4 and len(day4_forecasts) < 7:
        day4_forecasts.append(line)
      elif date == day5 and len(day5_forecasts) < 7:
        day5_forecasts.append(line)
      
    # Format output (moved outside the loop for efficiency)
    forecast_txt = "**📆 Today's Forecast**\n" + "\n".join(today_forecasts)
    forecast_txt += f"\n\n**📅 {tomorrow.strftime('%a %b %d')}'s Forecast**\n" + "\n".join(tomorrow_forecasts)
    forecast_txt += f"\n\n**📅 {day3.strftime('%a %b %d')}'s Forecast**\n" + "\n".join(day3_forecasts)
    forecast_txt += f"\n\n**📅 {day4.strftime('%a %b %d')}'s Forecast**\n" + "\n".join(day4_forecasts)
    forecast_txt += f"\n\n**📅 {day5.strftime('%a %b %d')}'s Forecast**\n" + "\n".join(day5_forecasts)
    
    return forecast_txt

if __name__ == "__main__":
    print("⏰ Running weather bot...")
    current = get_weather(CITY)
    forecast = get_forecast(CITY)
    message = f"{current}\n{forecast}"
    send_daily_weather()

    
