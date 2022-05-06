import requests
from timezonefinder import TimezoneFinder
from ..config import ERROR_MESSAGE


def get_city_coordinates(city: str):
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search.php?q={city}&format=jsonv2")
    data = response.json()
    if not len(data):
        raise ValueError('City not found.')

    lon = float(data[0]['lon'])
    lat = float(data[0]['lat'])

    return lat, lon


def get_place_from_coords(lat, long):
    response = requests.get(
        f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={long}&format=json&zoom=10&addressdetails=0&accept-language=en')

    if response.status_code != 200:
        raise ValueError(ERROR_MESSAGE)

    response = response.json()
    place = response['display_name'].split(',')[0]
    return place


def get_country_from_coords(lat, long):
    response = requests.get(
        f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={long}&format=json&zoom=3&addressdetails=0&accept-language=en')

    if response.status_code != 200:
        raise ValueError(ERROR_MESSAGE)

    response = response.json()
    country = response['display_name']
    return country


def get_timezone_from_coords(lat, long):
    tf = TimezoneFinder()
    zone_name = tf.timezone_at(lng=long, lat=lat)
    return zone_name
