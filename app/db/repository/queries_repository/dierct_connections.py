from app.db.database import driver


def check_direct_connection(device_id_1, device_id_2):
    try:
        with driver.session() as session:
            query = """
            MATCH (a:Device)-[r:CONNECTED]->(b:Device)
            WHERE a.id = $device_id_1 AND b.id = $device_id_2
            RETURN COUNT(r) > 0 AS is_connected
            """
            result = session.run(query, {"device_id_1": device_id_1, "device_id_2": device_id_2})

            record = result.single()

            if record:

                return {"is_connected": record["is_connected"]}
            else:
                return {"is_connected": False}

    except Exception as e:
        return {"error": "Database Error", "details": str(e)}