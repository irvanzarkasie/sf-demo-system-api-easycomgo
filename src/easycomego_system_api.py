import sys
import json
from flask import Flask, request, jsonify, make_response, Response
from flask_restful import Api, Resource
import pprint
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import uuid
import socket
from datetime import datetime, timedelta
import os
import urllib3

app = Flask(__name__)
api = Api(app)

# CONSTANTS
api_host = socket.gethostname()
api_port = 35010
api_id = "easycomego_system_api"

# Work directory setup
script_dir = os.path.dirname(os.path.realpath(__file__))
home_dir = "/".join(script_dir.split("/")[:-1])
log_dir = "{home_dir}/logs".format(home_dir=home_dir)

# HTTP connection pool
http = urllib3.PoolManager()

# Hash map for departure/destination code
DEPDESTCODEMAP = {
  "EASY-MY-PRT-KLANG": "MY-01",
  "EASY-MY-BU": "MY-02",
  "EASY-SG-HF": "SG-01",
  "EASY-SG-BV": "SG-02"
}

# Hash map for transport type code
TRANSTYPECODEMAP = {
   "BUS": "9001",
   "SHIP": "9002",
   "VAN": "9003",
   "MPV": "9004",
   "EXEC_TAXI": "9005"
}

class EasycomegoApi(Resource):
   def get(self, transport_type):
      # Parse arguments
      args = request.args
      departure_code = args.get("departureCode", None)
      destination_code = args.get("destinationCode", None)

      resp = http.request("GET", "http://168.119.225.15:39000/getRoutes")
      resp_payload = json.loads(resp.data.decode("utf-8"))

      resp_list = []
      for route in resp_payload:
         dep_code = route.get("departureCode")
         dest_code = route.get("destinationCode")
         trans_code = route.get("transportCode")
         mapped_dep_code = DEPDESTCODEMAP.get(dep_code, "")
         mapped_dest_code = DEPDESTCODEMAP.get(dest_code, "")
         mapped_trans_code = TRANSTYPECODEMAP.get(trans_code, "")

         if transport_type is not None and departure_code is not None and destination_code is not None:
            if transport_type == mapped_trans_code and departure_code == mapped_dep_code and destination_code == mapped_dest_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is None and departure_code is not None and destination_code is not None:
            if departure_code == mapped_dep_code and destination_code == mapped_dest_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is not None and departure_code is None and destination_code is not None:
            if transport_type == mapped_trans_code and destination_code == mapped_dest_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is not None and departure_code is not None and destination_code is None:
            if transport_type == mapped_trans_code and departure_code == mapped_dep_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is None and departure_code is None and destination_code is not None:
            if destination_code == mapped_dest_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is None and departure_code is not None and destination_code is None:
            if departure_code == mapped_dep_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is not None and departure_code is None and destination_code is None:
            if transport_type == mapped_trans_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif transport_type is None and departure_code is None and destination_code is None:
            resp_list.append({
               "transportCode":  mapped_trans_code,
               "departureCode": mapped_dep_code,
               "destinationCode": mapped_dest_code
            })
         # end if
         else:
            resp_list.append({
               "transportCode":  mapped_trans_code,
               "departureCode": mapped_dep_code,
               "destinationCode": mapped_dest_code
            })
         # end else
      # end for

      return jsonify(resp_list)
   # end def
# end class

class EasycomegoApiDefault(Resource):
   def get(self):
      # Parse arguments
      args = request.args
      departure_code = args.get("departureCode", None)
      destination_code = args.get("destinationCode", None)

      resp = http.request("GET", "http://168.119.225.15:39000/getRoutes")
      resp_payload = json.loads(resp.data.decode("utf-8"))

      resp_list = []
      resp_list = []
      for route in resp_payload:
         dep_code = route.get("departureCode")
         dest_code = route.get("destinationCode")
         trans_code = route.get("transportCode")
         mapped_dep_code = DEPDESTCODEMAP.get(dep_code, "")
         mapped_dest_code = DEPDESTCODEMAP.get(dest_code, "")
         mapped_trans_code = TRANSTYPECODEMAP.get(trans_code, "")

         if departure_code is not None and destination_code is not None:
            if departure_code == mapped_dep_code and destination_code == mapped_dest_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif departure_code is not None and destination_code is None:
            if departure_code == mapped_dep_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         elif departure_code is None and destination_code is not None:
            if destination_code == mapped_dest_code:
               resp_list.append({
                  "transportCode":  mapped_trans_code,
                  "departureCode": mapped_dep_code,
                  "destinationCode": mapped_dest_code
               })
            # end if
         # end if
         else:
            resp_list.append({
               "transportCode":  mapped_trans_code,
               "departureCode": mapped_dep_code,
               "destinationCode": mapped_dest_code
            })
         # end else
      # end for

      return jsonify(resp_list)
   # end def
# end class

api.add_resource(EasycomegoApi, '/sys/easycomeeasygo/booking/<transport_type>/routes')
api.add_resource(EasycomegoApiDefault, '/sys/easycomeeasygo/booking/routes')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=api_port)
# end if