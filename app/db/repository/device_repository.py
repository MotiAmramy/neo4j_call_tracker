from returns.maybe import Maybe, Nothing
from returns.result import Success, Failure

from app.db.database import driver
from app.db.models.device import Device





def insert_device(device: Device):
    with driver.session() as session:
        try:
            query = """
            CREATE (device:Device {
                device_id: $device_id, brand: $brand, model: $model, os: $os, 
                location: $location, id: $id})
            RETURN device.id
            """

            params = {
                "device_id": device.device_id,
                "brand": device.brand,
                "model": device.model,
                "os": device.os,
                "location": device.location,

            }
            res = session.run(query, params).single()
            return Success(res['device.id'])

        except Exception as e:
            print(str(e))
            return Failure(str(e))
