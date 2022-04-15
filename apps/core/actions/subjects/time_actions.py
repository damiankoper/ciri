from datetime import datetime, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from timezonefinder import TimezoneFinder
import pytz

from ..utils import (get_city_coordinates,
                     string_to_num_of_days, create_default_json_response)


class ActionTimeDefaultLocation(Action):

    def name(self) -> Text:
        return "action_time_default_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        response = create_default_json_response(
            f"Current local time is {current_time}.")
        dispatcher.utter_message(json_message=response)

        return []


class ActionDayToday(Action):
    def name(self) -> Text:
        return "action_day_today"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day = datetime.today().strftime('%A')
        response = create_default_json_response(f"Today is {day}.")
        dispatcher.utter_message(json_message=response)

        return []


class ActionDateRelative(Action):
    def name(self) -> Text:
        return 'action_date_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        # number of days is always last in entities array
        number_of_days_string = date_only[-1]['value']
        number_of_days = string_to_num_of_days(number_of_days_string)
        day_and_date = (datetime.today() +
                        timedelta(days=number_of_days)).strftime('%A, %d %B %Y')
        response = create_default_json_response(f"It will be {day_and_date}.")
        dispatcher.utter_message(json_message=response)

        return []


class ActionDateAndTime(Action):
    def name(self) -> Text:
        return "action_date_and_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day_and_time = datetime.now().strftime('%H:%M, %A %d %B %Y')
        response = create_default_json_response(f"It is now {day_and_time}.")
        dispatcher.utter_message(json_message=response)

        return []


class ActionTimeCustomLocation(Action):
    def name(self) -> Text:
        return "action_time_custom_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        city = gpe_only[0]['value']

        try:
            lat, lon = get_city_coordinates(city)
        except Exception as err:
            dispatcher.utter_message(json_message=err)
            return []

        tf = TimezoneFinder()
        zone_name = tf.timezone_at(lng=lon, lat=lat)
        response = datetime.now(pytz.timezone(
            zone_name)).strftime('%H:%M, %A %d %B %Y')

        dispatcher.utter_message(
            json_message=create_default_json_response(response))

        return []