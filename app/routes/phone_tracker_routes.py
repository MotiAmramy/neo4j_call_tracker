from flask import Blueprint

from app.services.all_connection_by_device_id import count_connected_devices
from app.services.bluetooth_path import find_bluetooth_connected_devices
from app.services.intractions_flow import flow_of_insert_devices, flow_of_connect_devices, check_if_got_same_ids
from app.services.signle_strong_then_60 import get_strong_device_connections

phone_blueprint = Blueprint("phone_tracker", __name__)

from flask import jsonify, request


@phone_blueprint.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   try:
      data = request.json

      if not data or check_if_got_same_ids(data):
         return jsonify({"error": "No correct data or no data provided"}), 400

      flow_of_insert_devices(data['devices'])
      flow_of_connect_devices(data['interaction'])
      return jsonify({"message": "Devices and interaction processed successfully"}), 200

   except Exception as e:
      print(str(e))
      return jsonify({"error": f"Unexpected error: {str(e)}"}), 500





@phone_blueprint.route('/api/bluetooth_path', methods=['GET'])
def get_device_connections():
   try:
      data = find_bluetooth_connected_devices()

      return jsonify(data), 200

   except Exception as e:
      print(f"Error: {str(e)}")
      return jsonify({"error": "Unexpected error occurred"}), 500






@phone_blueprint.route('/api/strong_device_connections', methods=['GET'])
def get_strong_device():
   try:
      data = get_strong_device_connections()
      return jsonify(data), 200

   except Exception as e:
      print(f"Error: {str(e)}")
      return jsonify({"error": "Unexpected error occurred"}), 500


@phone_blueprint.route('/api/count_connected_devices', methods=['GET'])
def count_connected():
    try:
      device_id = request.args.get('device_id')

      if not device_id:
         return jsonify({"error": "Device ID is required"}), 400


      data = count_connected_devices(device_id)
      return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Database Error", "details": str(e)}), 500
