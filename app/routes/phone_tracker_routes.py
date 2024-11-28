from flask import Blueprint

from app.db.repository.queries_repository.all_connection_by_device_id import count_connected_devices
from app.db.repository.queries_repository.bluetooth_path import find_bluetooth_connected_devices
from app.db.repository.queries_repository.dierct_connections import check_direct_connection
from app.db.repository.queries_repository.recent_interaction_device import get_most_recent_interaction
from app.db.repository.queries_repository.signle_strong_then_60 import get_strong_device_connections
from app.services.intractions_flow import flow_of_insert_devices, flow_of_connect_devices, check_if_got_same_ids
from flask import jsonify, request


phone_blueprint = Blueprint("phone_tracker", __name__)



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




@phone_blueprint.route('/api/check_direct_connection', methods=['GET'])
def check_connection():
    try:
        device_id_1 = request.args.get('device_id_1')
        device_id_2 = request.args.get('device_id_2')
        if not device_id_1 or not device_id_2:
            return jsonify({"error": "Both device IDs are required"}), 400
        data = check_direct_connection(device_id_1, device_id_2)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Unexpected Error", "details": str(e)}), 500




@phone_blueprint.route('/api/get_most_recent_interaction', methods=['GET'])
def recent_interaction():
    try:
        device_id = request.args.get('device_id')
        if not device_id:
            return jsonify({"error": "Device ID is required"}), 400

        data = get_most_recent_interaction(device_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Unexpected Error", "details": str(e)}), 500