import os

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')

ERROR_MESSAGE = {"type": "error",
                 "message": "Remote source error occured. Check input data"}

NO_COORDS_MSG = 'Location not provided. Make sure to give location permission to your browser or specify your location in question.'

class LocationNotProvided(Exception):
    pass
