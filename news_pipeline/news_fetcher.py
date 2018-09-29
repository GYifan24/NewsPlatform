import logging
import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jeonsbco:z6ls7E4CF4HgCKMhWaOF-_f6MyIO9IzT@otter.rmq.cloudamqp.com/jeonsbco"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrapeNews"

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://zzhqzyxc:a5qM8Ik5J0Y1pw6pPKuuM8o0Rs8DjvKH@otter.rmq.cloudamqp.com/zzhqzyxc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "dedupeQueue"

SLEEP_TIME_IN_SECONDS = 5 * 60

logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('news_fetcher')
logger.setLevel(logging.DEBUG)

scrape_news_queue_client  = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client  = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if not isinstance(msg, dict):
        logger.warning('message is broken')
        return

    text = None

    article = Article(msg['url'])
    article.download()
    article.parse()

    msg['text'] = article.text
    dedupe_news_queue_client.sendMessage(msg)


def run():
    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()

            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    logger.warning(e)
                    pass
            scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()
