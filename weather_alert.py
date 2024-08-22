import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_location():
    """Fetch current location based on IP address."""
    response = requests.get('http://ipinfo.io')
    data = response.json()
    return data['city'], data['region']

def get_weather(city):
    """Get weather data from WeatherAPI."""
    url = f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=1'
    response = requests.get(url)
    return response.json()

def send_telegram_message(message):
    """Send a message to a Telegram chat via the bot."""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message. Error: {response.status_code}, {response.text}')

def check_weather_conditions(weather_data):
    """Check for specific weather conditions (rain, wind, heat, cold)."""
    forecast_day = weather_data['forecast']['forecastday'][0]['day']
    condition = forecast_day['condition']['text'].lower()
    max_temp = forecast_day['maxtemp_f']
    min_temp = forecast_day['mintemp_f']
    max_wind = forecast_day['maxwind_mph']

    alert_messages = []

    # Check for rain
    if 'rain' in condition:
        alert_messages.append(f"Alert! It's going to rain today. Condition: {condition.capitalize()}")
    
    # Check for wind > 25 mph
    if max_wind > 25:
        alert_messages.append(f"Alert! It's going to be windy today. Max wind: {max_wind} mph")

    # Check for heat > 90°F
    if max_temp > 85:
        alert_messages.append(f"Alert! It's going to be hot today. Max temp: {max_temp}°F")
    
    # Check for cold < 60°F
    if min_temp < 60:
        alert_messages.append(f"Alert! It's going to be cold today. Min temp: {min_temp}°F")

    # Combine all alerts into one message
    if alert_messages:
        return "\n".join(alert_messages)
    return None

def main():
    city, region = get_location()
    print(f"Checking weather for: {city}, {region}")
    
    # Get weather data
    weather_data = get_weather(city)
    
    # Check today's weather conditions for alert
    alert_message = check_weather_conditions(weather_data)
    if alert_message:
        send_telegram_message(alert_message)

if __name__ == "__main__":
    main()
