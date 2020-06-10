import requests

import config


class ApiMediaWiki:

    URL_API_MEDIAWIKI = config.URL_MEDIA_WIKI
    PARAM_SEARCH = config.PARAM_MEDIA_WIKI_SEARCH
    PARAM_PAGE = config.PARAM_MEDIA_WIKI_PAGE

    def __init__(self, place_to_find):
        self.place = place_to_find

    # def get_url(self):
    #     for key, value in self.PARAM_MEDIA_WIKI.items():
    #         params += "{}={}&".format(key, value)
    #     params += "titles={}".format(self.place.replace(" ", "_"))
    #     url = "{}?{}".format(self.URL_API_MEDIAWIKI, params)
    #     print(url)
    #     return url

    def get_data_from_wiki(self):
        list_searchs = self.get_data_from_search()
        page_id = list_searchs[0]['pageid']
        return self.get_data_from_page(page_id)[:600]

    def get_data_from_search(self):

        try:
            params = self.PARAM_SEARCH
            params["srsearch"] = self.place
            res = requests.get(url=self.URL_API_MEDIAWIKI, params=params)
            response = res.json()

            list_searchs = response['query']['search']

            return list_searchs

        except requests.exceptions.RequestException as e:
            print('ERROR: {}'.format(e))
            return "La requête mediawiki n'a pas abouti."

    def get_data_from_page(self, page_id):
        try:
            params = self.PARAM_PAGE
            params["pageids"] = page_id
            res = requests.get(url=self.URL_API_MEDIAWIKI, params=params)
            response = res.json()

            return response['query']['pages'][0]['extract']

        except requests.exceptions.RequestException as e:
            print('ERROR: {}'.format(e))
            return "La requête mediawiki n'a pas abouti."
