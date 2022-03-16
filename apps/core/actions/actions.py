# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime
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
    response = f"Current local time is {current_time}"
    dispatcher.utter_message(text=response)

    return []
