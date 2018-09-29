import json
import os
import pickle
import redis
import sys
import logging

from bson.json_util import dumps

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

REDIS_HOST = "localhost"
REDIS_PORT = 6379

NEWS_LIMIT = 200
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 60 * 60

NEWS_TABLE_NAME = "news"

redis_client = redis.StrictRedis()

LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=LOGGER_FORMAT)
LOGGER = logging.getLogger('backend_service')
LOGGER.setLevel(logging.DEBUG)

def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    LOGGER.debug(news)
    return json.loads(dumps(news))


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)

    if page_num <= 0:
        return []

    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # The final list of news to be returned.
    sliced_news = []
    db = mongodb_client.get_db()


    if redis_client.get(user_id) is not None:
        LOGGER.debug("user exist in redis")
        # desirialize
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index:end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        LOGGER.debug("fetch news from database and saved in redis")
        # Read latest news from database
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        # Save latest news's digest
        total_news_digests = [x['digest'] for x in total_news]

        # save serialized data in redis
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']

    return json.loads(dumps(sliced_news))
