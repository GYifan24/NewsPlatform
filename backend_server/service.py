""" Backend service """
import logging
import operations

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=LOGGER_FORMAT)
LOGGER = logging.getLogger('backend_service')
LOGGER.setLevel(logging.DEBUG)


def add(num1, num2):
    """ Test method """
    LOGGER.debug("add is called with %d and %d", num1, num2)
    return num1 + num2


def get_one_news():
    """ Test method to get one news """
    LOGGER.debug("getOneNews is called")
    return operations.getOneNews()


def getNewsSummariesForUser(user_id, page_num):
    """ Get news summaries for a user """
    LOGGER.debug("getNewsSummariesForUser is called with %s and %s", user_id, page_num)
    return operations.getNewsSummariesForUser(user_id, page_num)

def logNewsClickForUser(user_id, news_id):
    """ Log a news click event for a user. """
    LOGGER.debug("logNewsClickForUser is called with %s and %s", user_id, news_id)
    return operations.logNewsClickForUser(user_id, news_id)


# Threading RPC Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'getOneNews')
RPC_SERVER.register_function(getNewsSummariesForUser, 'getNewsSummariesForUser')
RPC_SERVER.register_function(logNewsClickForUser, 'logNewsClickForUser')

LOGGER.info("Starting RPC server on %s:%d", SERVER_HOST, SERVER_PORT)

RPC_SERVER.serve_forever()
