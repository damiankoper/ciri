from time import time
import pytz
from datetime import date, timedelta, datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from ..utils.weather import get_forecast
from ..utils.location import get_city_coordinates, get_place_from_coords, get_timezone_from_coords
from ..utils.datetime import get_relative_time
from ..utils.common import create_default_json_response
from ..config import ERROR_MESSAGE


class ActionWeatherDefaultLocationAndTime(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_and_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metadata = tracker.latest_message.get("metadata")
        place = get_place_from_coords(**metadata)

        zone_name = get_timezone_from_coords(**metadata)
        today = datetime.now(pytz.timezone(zone_name))

        response = get_forecast(today, place, **metadata)
        dispatcher.utter_message(
            json_message=create_default_json_response(response))

        return []


class ActionWeatherDefaultLocationRelativeTime(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_relative_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        metadata = tracker.latest_message.get("metadata")
        place = get_place_from_coords(**metadata)
        zone_name = get_timezone_from_coords(**metadata)
        today = datetime.now(pytz.timezone(zone_name))


        if date_only:
            relative_time = date_only[0]['value'].lower()
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot detect for which day you want weather forecast.'))
            return []

        try:
            number_of_days = get_relative_time(relative_time)
        except ValueError:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot detect number of days'))
            return []

        searched_date = today + timedelta(days=number_of_days)

        try:
            response = get_forecast(searched_date, place, **metadata)
        except ValueError:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []

        dispatcher.utter_message(
            json_message=create_default_json_response(response))
        return []


class ActionWeatherCustomLocationDefaultTime(Action):
    def name(self) -> Text:
        return 'action_weather_custom_location_default_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        if gpe_only:
            city = gpe_only[0]['value']
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot properly detect given place. Try another one.'))
            return []

        try:
            lat, lon = get_city_coordinates(city)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        zone_name = get_timezone_from_coords(lat, lon)
        today = datetime.now(pytz.timezone(zone_name))

        try:
            response = get_forecast(today, city, lat, lon)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        dispatcher.utter_message(
            json_message=create_default_json_response(response))
        return []


class ActionWeatherCustomLocationRelativeTime(Action):
    def name(self) -> Text:
        return 'action_weather_custom_location_relative_time'

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

        if date_only:
            relative_time = date_only[0]['value'].lower()
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot detect for which day you want weather forecast.'))
            return []

        try:
            number_of_days = get_relative_time(relative_time)
        except ValueError:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot detect number of days'))
            return []

        try:
            lat, lon = get_city_coordinates(city)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        zone_name = get_timezone_from_coords(lat, lon)
        today = datetime.now(pytz.timezone(zone_name))
        searched_date = today + timedelta(days=number_of_days)

        try:
            response = get_forecast(searched_date, city, lat, lon)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        dispatcher.utter_message(
            json_message=create_default_json_response(response))
        return []
