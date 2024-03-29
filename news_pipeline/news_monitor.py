import datetime
import hashlib
import redis
import os
import sys
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client

from cloudAMQP_client import CloudAMQPClient

SLEEP_TIME_IN_SECONDS = 20 * 60
# news expired in 3 days
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jeonsbco:z6ls7E4CF4HgCKMhWaOF-_f6MyIO9IzT@otter.rmq.cloudamqp.com/jeonsbco"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrapeNews"

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_monitor')
logger.setLevel(logging.DEBUG)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
couldAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def run():
    while True:
        news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)

        num_of_new_news = 0

        for news in news_list:
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
            # news is not in redis
            # logger.info("digest%s", str(news_digest))
            if redis_client.get(news_digest) is None:
                num_of_new_news = num_of_new_news + 1
                news['digest'] = news_digest
                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                redis_client.set(news_digest, "True")
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)
                couldAMQP_client.sendMessage(news)

        logger.info("Fetched %d news.", num_of_new_news)
        couldAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)



if __name__ == "__main__":
    run()
