import sys
import json
from flask import Flask, request, jsonify, make_response, Response
import pprint
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import uuid
import socket
from datetime import datetime, timedelta
import os
from urllib3 import HTTPConnectionPool
from urllib3.exceptions import (
        MaxRetryError,
        ProxyError,
        ReadTimeoutError,
        SSLError,
        ProtocolError,
)
from urllib3.response import httplib
from urllib3.util.ssl_ import HAS_SNI
from urllib3.util.timeout import Timeout
from urllib3.util.retry import Retry
from urllib3._collections import HTTPHeaderDict

app = Flask(__name__)

# CONSTANTS
api_host = socket.gethostname()
api_port = 35010
api_id = "easycomego_system_api"

# Work directory setup
script_dir = os.path.dirname(os.path.realpath(__file__))
home_dir = "/".join(script_dir.split("/")[:-1])
log_dir = "{home_dir}/logs".format(home_dir=home_dir)

@app.route('/getRoutes', methods=['GET'])
def getRoutes():
  return jsonify(ROUTES_LIST)
# end def

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=api_port)
# end if