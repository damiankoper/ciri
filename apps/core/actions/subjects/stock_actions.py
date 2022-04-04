from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

from ..config import FINNHUB_API_KEY, ERROR_MESSAGE

class ActionStockPrice(Action):
    def name(self) -> Text:
        return 'action_stock_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        if len(entities) == 0:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []

        company_name = entities[0]['value'].replace(' ', '')
        response = requests.get(
            f'https://finnhub.io/api/v1/search?q={company_name}&token={FINNHUB_API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []

        # TODO - fix lowercase symbols handling
        # TODO - enhance symbol lookup
        print(response.json()['result'][0]['symbol'])
        return []


class ActionCurrencyPrice(Action):
    def name(self) -> Text:
        return 'action_currency_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        # TODO - make it detect only 'MONEY' named entities
        print(entities)
