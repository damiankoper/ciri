from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

from ..config import WEATHER_API_KEY, ERROR_MESSAGE
from ..utils import (get_forecast, get_city_coordinates,
                     get_relative_time, create_default_json_response)


class ActionWeatherDefaultLocationAndTime(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_and_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat=51.1&lon=17.0333&units=metric&appid={WEATHER_API_KEY}')
        print('default')

        if response.status_code != 200:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []
        response = response.json()

        overall = response['weather'][0]['main'].lower()
        temperature = response['main']['temp']
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']

        msg = f"Current weather in Wrocław: temperature: {overall} {temperature}°C, pressure: {pressure}hPa, humidity: {humidity}%."
        dispatcher.utter_message(
            json_message=create_default_json_response(msg))

        return []


class ActionWeatherDefaultLocationRelative(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        relative_time = date_only[0]['value'].lower()

        number_of_days = get_relative_time(relative_time)

        try:
            response = get_forecast(number_of_days)
        except Exception as err:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []

        dispatcher.utter_message(
            json_message=create_default_json_response(response))
        return []


class ActionWeatherCustomLocationRelative(Action):
    def name(self) -> Text:
        return 'action_weather_custom_location_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        city = gpe_only[0]['value']
        # default date is today
        number_of_days = 0

        if date_only:
            relative_time = date_only[0]['value'].lower()
            number_of_days = get_relative_time(relative_time)

        try:
            lat, lon = get_city_coordinates(city)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        try:
            response = get_forecast(number_of_days, lat, lon, city)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        dispatcher.utter_message(
            json_message=create_default_json_response(response))
        return []
