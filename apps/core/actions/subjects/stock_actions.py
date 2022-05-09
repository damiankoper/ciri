from datetime import datetime
from typing import Any, Text, Dict, List
from ..utils.common import create_default_json_response
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

from ..config import FINNHUB_API_KEY, ERROR_MESSAGE, POLYGON_API_KEY


class TickerNotDetected(Exception):
    pass


class ActionStockPrice(Action):
    def name(self) -> Text:
        return 'action_stock_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']

        try:
            if len(entities) == 0:
                raise TickerNotDetected()

            # Lookup ticker, name and currency
            company_name = entities[0]['value']
            response = requests.get(
                f'https://api.polygon.io/v3/reference/tickers?type=CS&market=stocks&search={company_name}&active=true&limit=1&apiKey={POLYGON_API_KEY}')
            response_json = response.json()

            if response.status_code != 200 or len(response_json['results']) == 0:
                raise TickerNotDetected()

            ticker = response_json['results'][0]['ticker']
            name = response_json['results'][0]['name']
            currency = response_json['results'][0]['currency_name']

            # Lookup price + time
            response = requests.get(
                f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}')
            response_json = response.json()
            print(response_json)

            price = response_json['c']

            msg = {}
            msg['type'] = 'stock'
            msg['name'] = name
            msg['price'] = price
            msg['currency'] = currency
            msg['time'] = response_json['t']
            msg['ticker'] = ticker
            dispatcher.utter_message(json_message=msg)

        except TickerNotDetected:
            dispatcher.utter_message(json_message=create_default_json_response(
                "The symbol of given stock or currency could not be found. Try to be more specific."
            ))

        return []


class ActionCurrencyPrice(Action):
    def name(self) -> Text:
        return 'action_currency_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # TODO: Opisać problemy z detekcją encji walut, mozliwe rozwiązania:
        # * lepszy model
        # * stablicowanie (nazwa, symbol) np (polish zloty, PLN) i fuzzy search
        #
        # zbyt złożone na ten zakres

        dispatcher.utter_message(json_message=create_default_json_response(
            "I'm sorry but I'm not capable of providing currency information now. Try again in the future."
        ))
