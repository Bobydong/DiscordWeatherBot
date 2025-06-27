import requests
import smtplib
from email.message import EmailMessage
import time
import schedule 
from datetime import datetime, timedelta
import os
print("Script started. Current local time is:", datetime.now().strftime("%H:%M")) #finds the enviornment's local time


API_KEY = os.getenv("API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CITY = "Livingston, NJ, US"
UNITS = "imperial"
SEND_TIME = "07:00" 
EMAIL = os.getenv("EMAIL")

def get_weather(city_name): #uses their 2.5 version bc that one is completely free
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

def send_email(subject, body, to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg["From"] = EMAIL
    msg['to'] = to
    msg.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        password = os.getenv("EMAIL_APP_PASSWORD")
        server.login(EMAIL, password)
        server.send_message(msg)
    print("Email sent to", to)
    #the email may be formatted weird becuase the get_weather function is formatted for discord specifically

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
    message = f"{current}\n\n{forecast}"
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
    today = now.date()
    tomorrow = today + timedelta(days=1)

    today_forecasts = []
    tomorrow_forecasts = []

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
      elif date == tomorrow and len(tomorrow_forecasts) < 4:
        tomorrow_forecasts.append(line)

       # Format output
      forecast_txt = "**📆 Today's Forecast**\n" + "\n".join(today_forecasts[:4])
      forecast_txt += "\n\n**📅 Tomorrow's Forecast**\n" + "\n".join(tomorrow_forecasts)

    return forecast_txt


#=====scheduling====== 
schedule.every().day.at(SEND_TIME).do(send_daily_weather)



#=========Run it===========
#send_email(subject="Weather Update", body = get_weather("Livingston, NJ, US"), to = "chiangyienne17@gmail.com")
#send_discord_message(DISCORD_WEBHOOK_URL, get_weather(CITY))
#send_daily_weather()
while True:
    print(datetime.now().strftime("%H:%M") + f"✅ Scheduled to send at {SEND_TIME}. Waiting for time match...")
    schedule.run_pending()
    time.sleep(60)


