# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime, timedelta
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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
