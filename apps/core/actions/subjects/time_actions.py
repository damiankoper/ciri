from multiprocessing.sharedctypes import Value
import pytz
from datetime import datetime, timedelta, date
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from ..utils.location import get_city_coordinates, get_place_from_coords, get_timezone_from_coords
from ..utils.datetime import get_relative_time
from ..utils.common import create_default_json_response
from ..config import NO_COORDS_MSG, LocationNotProvided


class ActionTimeDefaultLocation(Action):

    def name(self) -> Text:
        return "action_time_default_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            metadata = tracker.latest_message.get("metadata")
            if(metadata['lat'] is None or metadata['long'] is None):
                raise LocationNotProvided()

            place = get_place_from_coords(**metadata)

            zone_name = get_timezone_from_coords(**metadata)
            time = datetime.now(pytz.timezone(zone_name)).strftime('%H:%M')

            dispatcher.utter_message(
                json_message=create_default_json_response(f'In {place} it is now {time}'))

        except ValueError as err:
            dispatcher.utter_message(json_message=err.args[0])

        except LocationNotProvided as err:
            dispatcher.utter_message(
                json_message=create_default_json_response(NO_COORDS_MSG))

        return []


class ActionDayToday(Action):
    def name(self) -> Text:
        return "action_day_today"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metadata = tracker.latest_message.get("metadata")

        if(metadata['lat'] is None or metadata['long'] is None):
            dispatcher.utter_message(
                json_message=create_default_json_response(NO_COORDS_MSG))
            return []

        place = get_place_from_coords(**metadata)

        zone_name = get_timezone_from_coords(**metadata)
        day = datetime.now(pytz.timezone(zone_name)).strftime('%A')

        response = create_default_json_response(f"Today in {place} is {day}.")
        dispatcher.utter_message(json_message=response)

        return []


class ActionDateRelative(Action):
    def name(self) -> Text:
        return 'action_date_relative'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        date_only = list(filter(lambda x: x['entity'] == 'DATE', entities))

        try:
            metadata = tracker.latest_message.get("metadata")
            if(metadata['lat'] is None or metadata['long'] is None):
                raise LocationNotProvided()

            zone_name = get_timezone_from_coords(**metadata)

            # number of days is always last in entities array
            if date_only:
                number_of_days_string = date_only[-1]['value']
            else:
                dispatcher.utter_message(json_message=create_default_json_response(
                    "Could not detect the number of days."))
                return []

            number_of_days = get_relative_time(number_of_days_string)


            today = datetime.now(pytz.timezone(zone_name))
            day_and_date = (today +
                            timedelta(days=number_of_days)).strftime('%A, %d %B %Y')
            response = create_default_json_response(
                f"It {'will be' if number_of_days > 0 else 'was'} {day_and_date}.")
            dispatcher.utter_message(json_message=response)

        except ValueError as err:
            dispatcher.utter_message(json_message=create_default_json_response(
                "Could not detect the number of days."))

        except LocationNotProvided:
            dispatcher.utter_message(
                json_message=create_default_json_response(NO_COORDS_MSG))

        return []


class ActionDateAndTime(Action):
    def name(self) -> Text:
        return "action_date_and_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metadata = tracker.latest_message.get("metadata")
        if(metadata['lat'] is None or metadata['long'] is None):
            dispatcher.utter_message(
                json_message=create_default_json_response(NO_COORDS_MSG))
            return []

        place = get_place_from_coords(**metadata)

        zone_name = get_timezone_from_coords(**metadata)
        time = datetime.now(pytz.timezone(zone_name)
                            ).strftime('%H:%M, %A %d %B %Y')
        response = create_default_json_response(
            f"In {place} it is now {time}.")
        dispatcher.utter_message(json_message=response)

        return []


class ActionTimeCustomLocation(Action):
    def name(self) -> Text:
        return "action_time_custom_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        gpe_only = list(filter(lambda x: x['entity'] == 'GPE', entities))

        if gpe_only:
            city = gpe_only[0]['value']
        else:
            dispatcher.utter_message(json_message=create_default_json_response(
                'I cannot properly detect given place. Try another one.'))
            return []

        try:
            lat, lon = get_city_coordinates(city)
        except ValueError as err:
            dispatcher.utter_message(json_message=err.args[0])
            return []

        zone_name = get_timezone_from_coords(lat, lon)
        response = datetime.now(pytz.timezone(
            zone_name)).strftime('%H:%M, %A %d %B %Y')

        dispatcher.utter_message(
            json_message=create_default_json_response(f'In {city.capitalize()} it is now {response}'))

        return []
