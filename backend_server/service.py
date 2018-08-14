""" Backend service """
import logging
import json
import sys
import os


from bson.json_util import dumps
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
import mongodb_client
# import operations

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

def getOneNews():
    LOGGER.debug("getOneNews is called")
    res = mongodb_client.get_db()['news'].find_one()
    return json.loads(dumps(res))

# Threading RPC Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(getOneNews, 'getOneNews')
# RPC_SERVER.register_function(get_one_news, 'getOneNews')

LOGGER.info("Starting RPC server on %s:%d", SERVER_HOST, SERVER_PORT)

RPC_SERVER.serve_forever()
