import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from ..config import NEWS_API_KEY, ERROR_MESSAGE


class ActionNewsDefaultLocation(Action):

    def name(self) -> Text:
        return "action_news_default_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get(
            f'https://newsapi.org/v2/top-headlines?country=pl&pageSize=5&page=1&apiKey={NEWS_API_KEY}')
        if response.status_code != 200:
            dispatcher.utter_message(text=ERROR_MESSAGE)
            return []
        response = response.json()
        msg = {}
        msg['articles'] = response["articles"]
        msg['type'] = 'default location articles'
        dispatcher.utter_message(json_message=msg)
        return []
