from datetime import datetime, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from timezonefinder import TimezoneFinder
import pytz

from ..config import ERROR_MESSAGE
from ..utils import string_to_num_of_days


class ActionTimeDefaultLocation(Action):

    def name(self) -> Text:
        return "action_time_default_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        response = f"Current local time is {current_time}."
        dispatcher.utter_message(text=response)

        return []


class ActionDayToday(Action):
    def name(self) -> Text:
        return "action_day_today"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day = datetime.today().strftime('%A')
        response = f"Today is {day}."
        dispatcher.utter_message(text=response)

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
        response = f"It will be {day_and_date}."
        dispatcher.utter_message(text=response)

        return []


class ActionDateAndTime(Action):
    def name(self) -> Text:
        return "action_date_and_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        day_and_time = datetime.now().strftime('%H:%M, %A %d %B %Y')
        response = f"It is now {day_and_time}."
        dispatcher.utter_message(text=response)

        return []


class ActionTimeCustomLocation(Action):
    def name(self) -> Text:
        return "action_time_custom_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        data = []
        if len(gpe_only) > 0:
            user_choice = gpe_only[0]['value']
            # print(user_choice, tracker.latest_message)
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search.php?q={user_choice}&format=jsonv2")
            data = response.json()
        if not len(data):
            dispatcher.utter_message(text=ERROR_MESSAGE)
            return []

        lon = float(data[0]['lon'])
        lat = float(data[0]['lat'])

        tf = TimezoneFinder()
        zone_name = tf.timezone_at(lng=lon, lat=lat)
        response = datetime.now(pytz.timezone(
            zone_name)).strftime('%H:%M, %A %d %B %Y')

        dispatcher.utter_message(text=response)

        return []
