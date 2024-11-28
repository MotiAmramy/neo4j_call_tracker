from returns.result import Success, Failure
from app.db.database import driver
from app.db.models.device import Device



def insert_device(device: Device):
    with driver.session() as session:
        try:
            query = """
            MERGE (device:Device {
                id: $id, name: $name, brand: $brand, model: $model, os: $os, 
                latitude: $latitude, longitude: $longitude, altitude_meters: $altitude_meters, accuracy_meters: $accuracy_meters})
            RETURN device.id
            """
            params = {
                "id": device.id,
                "name": device.name,
                "brand": device.brand,
                "model": device.model,
                "os": device.os,
                "latitude": device.location.get('latitude', None),
                "longitude": device.location.get('longitude', None),
                "altitude_meters": device.location.get('altitude_meters', None),
                "accuracy_meters": device.location.get('accuracy_meters', None),
            }
            res = session.run(query, params).single()
            return Success(res['device.id'])
        except Exception as e:
            print(str(e))
            return Failure(str(e))




