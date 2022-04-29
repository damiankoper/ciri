import requests
from datetime import date, timedelta
from ..config import WEATHER_API_KEY, ERROR_MESSAGE

def get_forecast(number_of_days: int, place: str, lat: float, long: float):
    if number_of_days > 7:
        raise ValueError(
            "I am sorry, but I cannot forecast weather for longer than seven days.")

    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude=current,minutely,hourly,alerts&units=metric&appid={WEATHER_API_KEY}')

    if response.status_code != 200:
        raise ValueError(ERROR_MESSAGE)

    response = response.json()
    searched_date = date.today() + timedelta(days=number_of_days)

    msg = ''
    for item in response['daily']:
        if date.fromtimestamp(item['dt']) == searched_date:
            day = searched_date.strftime('%A, %d %B %Y')
            overall = item['weather'][0]['main'].lower()
            temperature = item['temp']['day']
            pressure = item['pressure']
            humidity = item['humidity']
            msg = f"Weather forecast for {place} for {day}. It will be {overall}, with temperature {temperature}°C, air pressure equal to {pressure}hPa and humidity {humidity}%."
    return msg
