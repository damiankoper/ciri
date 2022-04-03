# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import date, datetime, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from timezonefinder import TimezoneFinder
import pytz

from .config import WEATHER_API_KEY, FINNHUB_API_KEY, ERROR_MESSAGE
from .utils import string_to_num_of_days, next_weekday


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


class ActionStockPrice(Action):
    def name(self) -> Text:
        return 'action_stock_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        if len(entities) == 0:
            dispatcher.utter_message(text=ERROR_MESSAGE)
            return []

        company_name = entities[0]['value'].replace(' ', '')
        response = requests.get(
            f'https://finnhub.io/api/v1/search?q={company_name}&token={FINNHUB_API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text=ERROR_MESSAGE)
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


class ActionWeatherDefaultLocationAndTime(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_and_time'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat=51.1&lon=17.0333&units=metric&appid={WEATHER_API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text="Remote source error occured")
            return []
        response = response.json()

        overall = response['weather'][0]['main'].lower()
        temperature = response['main']['temp']
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']

        msg = f"Current weather in Wrocław: temperature: {overall} {temperature}°C, pressure: {pressure}hPa, humidity: {humidity}.%"
        dispatcher.utter_message(text=msg)

        return []


class ActionWeatherDefaultLocationRelative(Action):
    def name(self) -> Text:
        return 'action_weather_default_location_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        weekdays = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']

        relative_time = date_only[0]['value'].lower()

        if relative_time in weekdays:
            weekday_number = weekdays.index(relative_time)
            number_of_days = next_weekday(weekday_number)
        else:
            number_of_days = string_to_num_of_days(relative_time)

        if number_of_days > 7:
            dispatcher.utter_message(
                text="Cannot forecast weather for longer than seven days.")
            return []

        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat=51.1&lon=17.0333&exclude=current,minutely,hourly,alerts&units=metric&appid={WEATHER_API_KEY}')

        if response.status_code != 200:
            dispatcher.utter_message(text=ERROR_MESSAGE)
            return []

        response = response.json()
        searched_date = date.today() + timedelta(days=number_of_days)

        msg = 'ms'
        for item in response['daily']:
            if date.fromtimestamp(item['dt']) == searched_date:
                day = searched_date.strftime('%A, %d %B %Y')
                overall = item['weather'][0]['main'].lower()
                temperature = item['temp']['day']
                pressure = item['pressure']
                humidity = item['humidity']
                msg = f"Weather forecast for {day}: {overall}, {temperature}°C. Pressure: {pressure}hPa, humidity: {humidity}%."

        dispatcher.utter_message(text=msg)
        return []
