from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://ahuuvkig:8VOSWe6MSahwtnhRKzqrZ1n4Z3Tmrz-K@otter.rmq.cloudamqp.com/ahuuvkig"
QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sentMsg = {'test': 'test'}
    client.sendMessage(sentMsg)

    client.sleep(5)

    receiveMsg = client.getMessage()
    assert sentMsg == receiveMsg

    print("Good")

if __name__ == "__main__":
    test_basic()
