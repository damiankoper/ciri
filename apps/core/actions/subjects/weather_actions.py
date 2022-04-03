from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

from ..config import WEATHER_API_KEY, ERROR_MESSAGE
from ..utils import (get_forecast, string_to_num_of_days,
                     next_weekday, get_city_coordinates, get_relative_time)


class ActionWeatherDefaultLocationAndTime(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_and_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat=51.1&lon=17.0333&units=metric&appid={WEATHER_API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text="Remote source error occured")
            return []
        response = response.json()

        overall = response['weather'][0]['main'].lower()
        temperature = response['main']['temp']
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']

        msg = f"Current weather in Wrocław: temperature: {overall} {temperature}°C, pressure: {pressure}hPa, humidity: {humidity}.%"
        dispatcher.utter_message(text=msg)

        return []


class ActionWeatherDefaultLocationRelative(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        weekdays = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']

        relative_time = date_only[0]['value'].lower()

        if relative_time in weekdays:
            weekday_number = weekdays.index(relative_time)
            number_of_days = next_weekday(weekday_number)
        else:
            number_of_days = string_to_num_of_days(relative_time)

        if number_of_days > 7:
            dispatcher.utter_message(
                text="Cannot forecast weather for longer than seven days.")
            return []

        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat=51.1&lon=17.0333&exclude=current,minutely,hourly,alerts&units=metric&appid={WEATHER_API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text=ERROR_MESSAGE)
            return []

        response = response.json()
        searched_date = date.today() + timedelta(days=number_of_days)

        msg = 'ms'
        for item in response['daily']:
            if date.fromtimestamp(item['dt']) == searched_date:
                day = searched_date.strftime('%A, %d %B %Y')
                overall = item['weather'][0]['main'].lower()
                temperature = item['temp']['day']
                pressure = item['pressure']
                humidity = item['humidity']
                msg = f"Weather forecast for {day}: {overall}, {temperature}°C. Pressure: {pressure}hPa, humidity: {humidity}%."

        dispatcher.utter_message(text=msg)
        return []


class ActionWeatherDefaultLocationRelative(Action):
    def name(self) -> Text:
        return 'action_weather_custom_location_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        city = gpe_only[0]['value']
        relative_time = date_only[0]['value'].lower()

        number_of_days = get_relative_time(relative_time)

        try:
            lat, lon = get_city_coordinates(city)
        except Exception as err:
            dispatcher.utter_message(text=err)
            return []

        try:
            response = get_forecast(number_of_days, lat, lon)
        except Exception as err:
            dispatcher.utter_message(text=err)
            return []

        dispatcher.utter_message(text=response)
        return []
