import datetime
import logging
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
import news_topic_modeling_service_client

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jeonsbco:z6ls7E4CF4HgCKMhWaOF-_f6MyIO9IzT@otter.rmq.cloudamqp.com/jeonsbco"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrapeNews"


SLEEP_TIME_IN_SECONDS = 15

NEWS_TABLE_NAME = "news"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.6

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_deduper')
logger.setLevel(logging.DEBUG)

cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if not isinstance(msg, dict):
        logger.warning('message is broken')
        return

    text = msg['description']
    if text is None:
        return

    published_at = parser.parse(msg['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': {'$gte':published_at_day_begin,
                         '$lt':published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['description'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        # logger.debug("Pairwise Sim:%s", str(pairwise_sim))

        rows, _ = pairwise_sim.shape
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                logger.info("Duplicated news. Ignore.")
                return

    msg['publishedAt'] = parser.parse(msg['publishedAt'])

    description = msg['description']
    if description is None:
        description = msg['title']

    topic = news_topic_modeling_service_client.classify(description)
    msg['class'] = topic
    print("news topic: " + topic)
    db[NEWS_TABLE_NAME].replace_one({'digest':msg['digest']}, msg, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                # Parse and process the message
                try:
                    handle_message(msg)
                except Exception as e:
                    logger.warning(e)
                    pass

            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
