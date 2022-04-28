import requests
from word2number import w2n
from datetime import date, timedelta

from .config import WEATHER_API_KEY, ERROR_MESSAGE


def string_to_num_of_days(days_string: str):
    if 'day after tomorrow' in days_string:
        return 2
    elif 'day before yesterday' in days_string:
        return -2
    elif 'yesterday' in days_string :
        return -1
    elif 'tomorrow' in days_string:
        return 1
    elif days_string == 'week' or days_string == 'a week' in days_string:
        return 7
    elif 'week' in days_string:
        return 7 * w2n.word_to_num(days_string)
    else:
        return w2n.word_to_num(days_string)


def next_weekday(weekday: int):
    """weekday - number from 0 to 6, where 0 is Monday and 6 is Sunday"""
    today = date.today().weekday()
    days_ahead = weekday - today
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return days_ahead


def get_city_coordinates(city: str):
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search.php?q={city}&format=jsonv2")
    data = response.json()
    if not len(data):
        raise ValueError('City not found.')

    lon = float(data[0]['lon'])
    lat = float(data[0]['lat'])

    return lat, lon


def get_forecast(number_of_days: int = 0, lat: float = 51.1, lon: float = 17.033, city='Wrocław'):
    if number_of_days > 7:
        raise ValueError(
            "I am sorry, but I cannot forecast weather for longer than seven days.")

    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=metric&appid={WEATHER_API_KEY}')

    if response.status_code != 200:
        raise Exception(ERROR_MESSAGE)

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
            msg = f"Weather forecast for {city} for {day}. It will be {overall}, with temperature {temperature}°C, air pressure equal to {pressure}hPa and humidity {humidity}%."
    return msg


def get_relative_time(time_string: str):
    weekdays = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']

    relative_time = time_string.lower()
    possible_digits = [int(s) for s in relative_time.split() if s.isdigit()]

    if relative_time in weekdays:
        weekday_number = weekdays.index(relative_time)
        number_of_days = next_weekday(weekday_number)
    elif possible_digits:
        number_of_days = possible_digits[0]
    else:
        number_of_days = string_to_num_of_days(relative_time)

    return number_of_days


def get_number_of_days(days_string):
    days_string = days_string.lower()
    possible_digits = [int(s) for s in days_string.split() if s.isdigit()]

    if possible_digits:
        return possible_digits[0]
    else:
        return string_to_num_of_days(days_string)


def create_default_json_response(msg: str):
    return {
        "type": "default",
        "message": msg
    }
