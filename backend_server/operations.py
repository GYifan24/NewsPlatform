import json
import os
import pickle
import redis
import sys
import logging
from datetime import datetime

from bson.json_util import dumps

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client
import news_classes
from cloudAMQP_client import CloudAMQPClient

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

LOG_CLICKS_TASK_QUEUE_URL = "amqp://gkhhllta:nGhWDT6xqsWbB7zSGneO40bvggkTkXhl@otter.rmq.cloudamqp.com/gkhhllta"
LOG_CLICKS_TASK_QUEUE_NAME = "clickLog"
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

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

    # # Use preference to customize returned news news_list
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    # print("preference modle:" + preference)
    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if 'class' in news:
            news['class'] = news_classes.classes[news['class']]
        if 'class' in news and news['class'] == topPreference:
            news['reason'] = 'Recommend'

    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    msg = {'userId':user_id, 'newsId':news_id, 'timestamp':str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(msg);
