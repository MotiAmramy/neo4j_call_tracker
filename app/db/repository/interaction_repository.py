from app.db.database import driver










def create_interactions_connection(from_device_id, to_device_id, interaction):
    with driver.session() as session:
        try:
            query = """
            MATCH (a:Device {id: $from_device_id}), (b:Device {id: $to_device_id})
            CREATE (a)-[r:CONNECTED {
                distance_meters: $distance_meters,
                signal_strength_dbm: $signal_strength_dbm,
                timestamp: $timestamp,
                latitude: $latitude,
                longitude: $longitude,
                altitude_meters: $altitude_meters,
                accuracy_meters: $accuracy_meters
            }]->(b)
            RETURN r
            """
            params = {
                "from_device_id": from_device_id,
                "to_device_id": to_device_id,
                "method": interaction.method,
                "bluetooth_version": interaction.bluetooth_version,
                "signal_strength_dbm": interaction.signal_strength_dbm,
                "distance_meters": interaction.distance_meters,
                "duration_seconds": interaction.duration_seconds,
                "timestamp": interaction.timestamp
            }
            result = session.run(query, params)
            return result.single() is not None
        except Exception as e:
            print(f"Error creating connection: {str(e)}")
            return False

