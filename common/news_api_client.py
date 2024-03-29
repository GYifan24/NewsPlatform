import requests
import json

NEWS_API_ENDPOINT = "http://newsapi.org/v1/"
NEWS_API_KEY = "3c7c4cf3ba3f44eca5738255b8e216b8"
ARTICLES_API = "articles"

ARTICLES_API = 'articles'

CNN = 'cnn'

DEFAULT_SOURCES = [CNN]
SORT_BY_TOP = 'top'


def getNewsFromSources(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []

    for source in sources:
        payload = {
            'apiKey':NEWS_API_KEY,
            'source':source,
            'sortBy':sortBy}

        response = requests.get(NEWS_API_ENDPOINT + ARTICLES_API, params=payload)
        res_json = json.loads(response.content.decode('utf-8'))

        # Extract news from response.
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # Populate news source in each artical.
            for news in res_json['articles']:
                news['source'] = res_json['source']
        
        articles.extend(res_json['articles'])

    return articles
