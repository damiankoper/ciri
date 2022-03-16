# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime, timedelta
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from timezonefinder import TimezoneFinder
import pytz

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

class ActionDayTomorrow(Action):
  def name(self) -> Text:
    return "action_day_tomorrow"

  def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    day = (datetime.today() + timedelta(days=1)).strftime('%A')
    response = f"Tomorrow will be {day}."
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

    user_choice = tracker.get_slot("location")
    response = requests.get(f"https://nominatim.openstreetmap.org/search.php?q={user_choice}&format=jsonv2")
    data = response.json()

    if not len(data):
      dispatcher.utter_message(text="I don't know such city.")
      return []

    lon = data[0]['lon']
    lat = data[0]['lat']

    tf = TimezoneFinder()
    zone_name = tf.timezone_at(lng=lon, lat=lat)
    response = datetime.datetime.now(pytz.timezone(zone_name)).strftime('%H:%M, %A %d %B %Y')

    dispatcher.utter_message(text=response)

    return []
