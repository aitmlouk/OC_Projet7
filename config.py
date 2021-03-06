"""Constantes use by GrandPy."""

import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# ####### API #######

URL_GOOGLE = "https://maps.googleapis.com/maps/api/geocode/json"

KEY_GOOGLE = os.getenv("KEY_GOOGLE")

URL_MEDIA_WIKI = "https://fr.wikipedia.org/w/api.php"

# ####### API Parameters #######

# parameters of the mediawiki_search API request
PARAM_MEDIA_WIKI_SEARCH = {
    "action": "query",
    "format": "json",
    "list": "geosearch",
    "gsradius": 10000,
    "gslimit": 5
}

# parameters of the mediawiki_page API request
PARAM_MEDIA_WIKI_PAGE = {
    "action": "query",
    "prop": "extracts",
    "explaintext": 1,
    "format": "json",
    "formatversion": 2,
    "exlimit": 1,
    "exsentences": 5,
}

APP_ERROR = {
    "api_google_ko": -1,
    "api_google_bad_return": -2,
    "api_mediawiki_ko": -3,
    "api_mediawiki_bad_return": -2,
}

# ########## Test API Google ###########

# Expected value of the get_data_from_search function
API_GOOGLE_DATA_TEST = {"place_id": "123456", "lat": 10.1, "lng": 20.1}

# json returned by the google request
API_GOOGLE_JSON_FOR_TEST = {
    "results": [
        {
            "geometry": {
                "location": {
                    "lat": API_GOOGLE_DATA_TEST["lat"],
                    "lng": API_GOOGLE_DATA_TEST["lng"]
                }
            },
            "place_id": API_GOOGLE_DATA_TEST["place_id"],
        }
    ],
    "status": "OK"
}

# ########## Tests API MEDIA WIKI ###########

# Expected value of the get_data_from_search function
API_MEDIA_WIKI_SEARCH_FOR_TEST = {
    "title": "Lieu",
    "pageid": 123456,
    "lat": 10.1,
    "lng": 20.1
}

# Json returned by api mediawiki search
API_MEDIA_WIKI_SEARCH_JSON = {
    "query": {
        "geosearch": [
             {
                 "title": "Lieu",
                 "pageid": 123456,
                 "lat": 10.1,
                 "lng": 20.1,
             }
        ]
    }
}

# Expected value of the get_data_from_page function
API_MEDIA_WIKI_PAGE_FOR_TEST = "Page content"

API_MEDIA_WIKI_PAGE_JSON = {
    "query": {
        "pages": [
            {
                "pageid": 5043187,
                "ns": 0,
                "title": "Lieu",
                "extract": "Page content"
            }
        ]
    }
}
