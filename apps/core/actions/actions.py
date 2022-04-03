# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime, timedelta
from typing import Any, Text, Dict, List
from urllib import response
import urllib.parse

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from timezonefinder import TimezoneFinder
import pytz
from word2number import w2n
import os


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

    def string_to_num_of_days(self, days_string: str):
        if days_string == 'tomorrow':
            return 1
        elif days_string == 'week' or days_string == 'a week' in days_string:
            return 7
        elif 'week' in days_string:
            return 7 * w2n.word_to_num(days_string)
        else:
            return w2n.word_to_num(days_string)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        # number of days is always last in entities array
        number_of_days_string = date_only[-1]['value']
        number_of_days = self.string_to_num_of_days(number_of_days_string)

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
        print(list(map(lambda x: x['value'], entities)))
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        data = []
        if len(gpe_only) > 0:
            user_choice = gpe_only[0]['value']
            # print(user_choice, tracker.latest_message)
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search.php?q={user_choice}&format=jsonv2")
            data = response.json()
        if not len(data):
            dispatcher.utter_message(text="I don't know such city.")
            return []

        lon = float(data[0]['lon'])
        lat = float(data[0]['lat'])

        tf = TimezoneFinder()
        zone_name = tf.timezone_at(lng=lon, lat=lat)
        response = datetime.now(pytz.timezone(
            zone_name)).strftime('%H:%M, %A %d %B %Y')

        dispatcher.utter_message(text=response)

        return []


class ActionStockPrice(Action):
    def name(self) -> Text:
        return 'action_stock_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        if len(entities) == 0:
            dispatcher.utter_message(text="Company name not detected")
            return []

        API_KEY = os.environ.get('FINNHUB_API_KEY')
        company_name = entities[0]['value'].replace(' ', '')
        response = requests.get(
            f'https://finnhub.io/api/v1/search?q={company_name}&token={API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text="Company name not detected")
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


class ActionDefaultWeatherAndTIme(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_and_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        API_KEY = os.environ.get('WEATHER_API_KEY')
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat=51.1&lon=17.0333&units=metric&appid={API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text="Remote source error occured")
            return []
        response = response.json()

        msg = f"Weather in Wrocław: temperature: {response['main']['temp']}°C, pressure: {response['main']['pressure']}hPa, humidity: {response['main']['pressure']}%"
        dispatcher.utter_message(text=msg)

        return []
