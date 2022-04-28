from datetime import date, timedelta
from typing import Any, Text, Dict, List
from urllib import response
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

        response = get_forecast()
        dispatcher.utter_message(
            json_message=create_default_json_response(response))

        return []


class ActionWeatherDefaultLocationRelative(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        if date_only:
            relative_time = date_only[0]['value'].lower()
            number_of_days = get_relative_time(relative_time)
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot detect for which day you want weather forecast.'))
            return []

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

        if gpe_only:
            city = gpe_only[0]['value']
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot properly detect given place. Try another one.'))
            return []

        # default date is today
        number_of_days = 0

        if date_only:
            relative_time = date_only[0]['value'].lower()
            number_of_days = get_relative_time(relative_time)
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot detect for which day you want weather forecast.'))
            return []

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
