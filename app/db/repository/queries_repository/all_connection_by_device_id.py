from app.db.database import driver

def count_connected_devices(device_id):
    try:
        with driver.session() as session:
            query = """
            MATCH(a: Device)-[rel: CONNECTED]->(b:Device)
            WHERE b.id = $device_id
            RETURN COUNT(a) AS connected_devices_count
            """
            result = session.run(query, {"device_id": device_id})
            record = result.single()[0]
            return {'counted_connection': record}



    except Exception as e:
        return {"error": "Database Error", "details": str(e)}