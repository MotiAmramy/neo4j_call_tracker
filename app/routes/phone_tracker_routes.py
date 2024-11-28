from flask import Blueprint
import toolz as t

from app.db.models.device import Device
from app.db.models.interaction import Interaction
from app.db.repository.device_repository import insert_device
from app.services.intraction_service import flow_of_insert_devices, flow_of_connect_devices

phone_blueprint = Blueprint("phone_tracker", __name__)

from flask import jsonify, request


@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   try:
      data = request.json
      if not data:
         return jsonify({"error": "No data provided"}), 400
      data_inserted_devices = flow_of_insert_devices(data['devices'])
      flow_of_connect_devices(data_inserted_devices, data['interaction'])
      return jsonify({"message": "Devices and interaction processed successfully"}), 200

   except Exception as e:
      print(str(e))
      return jsonify({"error": f"Unexpected error: {str(e)}"}), 500




# @phone_blueprint.route("/api/bluetooth_connection", methods=['GET'])
# def get_bluetooth_interaction():
#    try:
