"""MediaWiki API Call Class."""

import random
import requests


import config


class ApiMediaWiki:
    """MediaWiki API Call Class.

    place : text ton analyze with api
    """
    URL_API_MEDIAWIKI = config.URL_MEDIA_WIKI
    PARAM_SEARCH = config.PARAM_MEDIA_WIKI_SEARCH
    PARAM_PAGE = config.PARAM_MEDIA_WIKI_PAGE
    TEXT_UNKNOW_RANDOM = [
        'Cet endroit ne me dis rien du tout, tu es sûr de ta question ?',
        'Je ne connais pas du tout ce lieu...',
        'COMMENT ???',
        'Je n\'entends plus très bien, mais ta question me semble bizarre !'
    ]
    TEXT_RESPONSE_RANDOM = [
        'Oui, je me souviens très bien de {}, il y a {} juste à côté,',
        'Ah {}, que de bons souvenirs, plus particulièrement {}',
        """Ca fait bien longtemps, mais je me rappelle de {}
        comme si c\'était hier. Je passais souvent à {}""",
        'J\'ai une anecdote sur {}, et surtout de mon passage à {}'
    ]

    APP_ERROR = config.APP_ERROR

    def __init__(self, place_to_find, lat, lng):
        self.place = place_to_find
        self.lat = lat
        self.lng = lng

    def get_data_from_wiki(self):
        """Method called by the /query route.
        returns :
        (content_page,
        url_link_wiki)
        """

        list_searchs = self.get_data_from_search()
        if list_searchs in self.APP_ERROR.values():
            return random.choice(self.TEXT_UNKNOW_RANDOM), "#"
        page_id = list_searchs["pageid"]
        title = list_searchs["title"]
        response_grandpy = self.get_random_text_response(self.place, title)
        content_page = self.get_data_from_page(page_id)
        url_link_wiki = self.get_url_wiki(title)
        return response_grandpy, content_page, url_link_wiki

    def get_data_from_search(self):
        """call the mediawiki API search with the place in parameter and return
        a list of pages corresponding to the place .
        [
            {
                "ns": 0,
                "title": "Lieu",
                "pageid": 123456,
                "snippet": "homonymes,..."
            }, ...
        """
        try:
            params = self.PARAM_SEARCH
            # params["srsearch"] = self.place
            params["gscoord"] = "{}|{}".format(self.lat, self.lng)
            res = requests.get(url=self.URL_API_MEDIAWIKI, params=params)
            if res.status_code == 200:
                response = res.json()
                list_searchs = random.choice(response["query"]["geosearch"])
                print("list", list_searchs)
                return list_searchs
            return self.APP_ERROR["api_mediawiki_ko"]
        except requests.exceptions.RequestException:
            return self.APP_ERROR["api_mediawiki_ko"]
        except KeyError:
            return self.APP_ERROR['api_mediawiki_bad_return']

    def get_data_from_page(self, page_id):
        """calls the mediawiki API for the requested location page.
        returns content of page"""
        try:
            payload = self.PARAM_PAGE
            payload["pageids"] = page_id
            res = requests.get(url=self.URL_API_MEDIAWIKI, params=payload)
            if res.status_code == 200:
                response = res.json()
                return response["query"]["pages"][0]["extract"]
            return self.APP_ERROR["api_mediawiki_ko"]
        except requests.exceptions.RequestException:
            return self.APP_ERROR["api_mediawiki_ko"]

    def get_url_wiki(self, title):
        """Returns the wikipedia link to display on the site."""
        url = "https://fr.wikipedia.org/wiki/{}".format(
            title.replace(" ", "_"))
        return url

    @classmethod
    def get_random_text_not_found(cls):
        """Return a random sentence if API don't find the place."""
        return random.choice(cls.TEXT_UNKNOW_RANDOM)

    def get_random_text_response(self, place, title):
        """Return a random response from Grandpy"""
        response_grandpy = random.choice(self.TEXT_RESPONSE_RANDOM)
        str_begin = "<strong>"
        str_end = "</strong>"
        return response_grandpy.format(str_begin + place.title() + str_end,
                                       str_begin + title + str_end)
