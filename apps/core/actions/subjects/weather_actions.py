from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from ..utils.weather import get_forecast
from ..utils.location import get_city_coordinates, get_place_from_coords
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

        response = get_forecast(number_of_days=0, place=place, **metadata)
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

        metadata = tracker.latest_message.get("metadata")
        place = get_place_from_coords(**metadata)

        try:
            response = get_forecast(number_of_days=number_of_days, place=place, **metadata)
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

        try:
            response = get_forecast(0, city, lat, lon)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
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

        try:
            response = get_forecast(number_of_days, city, lat, lon)
        except ValueError as err:
            dispatcher.utter_message(text=err.args[0])
            return []

        dispatcher.utter_message(
            json_message=create_default_json_response(response))
        return []
