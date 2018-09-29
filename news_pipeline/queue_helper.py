import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jeonsbco:z6ls7E4CF4HgCKMhWaOF-_f6MyIO9IzT@otter.rmq.cloudamqp.com/jeonsbco"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrapeNews"

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://zzhqzyxc:a5qM8Ik5J0Y1pw6pPKuuM8o0Rs8DjvKH@otter.rmq.cloudamqp.com/zzhqzyxc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "dedupeQueue"

def clearQueue(queue_url, queue_name):
    queue_client = CloudAMQPClient(queue_url, queue_name)

    num_of_messages = 0

    while True:
        if queue_client is not None:
            msg = queue_client.getMessage()
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1


if __name__ == "__main__":
    clearQueue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clearQueue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
