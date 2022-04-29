from itertools import count
import requests
import pycountry
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from ..config import NEWS_API_KEY, ERROR_MESSAGE
from ..utils.common import create_default_json_response
from ..utils.location import get_country_from_coords


class ActionNewsDefaultLocation(Action):

    def name(self) -> Text:
        return "action_news_default_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metadata = tracker.latest_message.get("metadata")
        country = get_country_from_coords(**metadata)

        country_code = pycountry.countries.get(name=country)

        response = requests.get(
            f'https://newsapi.org/v2/top-headlines?country={country_code.alpha_2}&pageSize=5&page=1&apiKey={NEWS_API_KEY}')
        if response.status_code != 200:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []
        response = response.json()

        msg = {}
        msg['articles'] = response["articles"]
        msg['type'] = 'default_location_articles'
        dispatcher.utter_message(json_message=msg)
        return []


class ActionNewsDefaultLocation(Action):

    def name(self) -> Text:
        return "action_news_custom_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        if gpe_only:
            country = gpe_only[0]['value']
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot properly detect given country. Try another one.'))
            return []

        country_code = pycountry.countries.get(name=country)

        response = requests.get(
            f'https://newsapi.org/v2/top-headlines?country={country_code.alpha_2}&pageSize=5&page=1&apiKey={NEWS_API_KEY}')
        if response.status_code != 200:
            dispatcher.utter_message(json_message=ERROR_MESSAGE)
            return []
        response = response.json()

        msg = {}
        msg['articles'] = response["articles"]
        msg['type'] = 'custom_location_articles'
        msg['location'] = country_code.official_name
        dispatcher.utter_message(json_message=msg)
        return []
