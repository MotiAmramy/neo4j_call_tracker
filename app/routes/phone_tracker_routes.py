from flask import Blueprint

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
      print(data)


      flow_of_connect_devices(data['interaction'], data_inserted_devices)
      return jsonify({"message": "Devices and interaction processed successfully"}), 200

   except Exception as e:
      print(str(e))
      return jsonify({"error": f"Unexpected error: {str(e)}"}), 500




# @phone_blueprint.route("/api/bluetooth_connection", methods=['GET'])
# def get_bluetooth_interaction():
#    try:
