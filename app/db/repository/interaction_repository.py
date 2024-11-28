from returns.result import Failure, Success

from app.db.database import driver
from app.db.models.interaction import Interaction


def create_interactions_connection(interaction: Interaction):
    with driver.session() as session:
        try:
            check_query = """
                      MATCH (a:Device)-[r:CONNECTED]->(b:Device)
                      WHERE r.timestamp = $timestamp
                      AND (a.id = $from_device_id OR b.id = $from_device_id)
                      AND (a.id = $to_device_id OR b.id = $to_device_id)
                      RETURN r
                      """
            check_params = {
                "from_device_id": interaction.from_device,
                "to_device_id": interaction.to_device,
                "timestamp": interaction.timestamp
            }
            existing_interaction = session.run(check_query, check_params).single()
            if existing_interaction:
                return Failure("Interaction already exists between the devices at the same timestamp.")
            query = """
            MATCH (a:Device {id: $from_device_id}), (b:Device {id: $to_device_id})
            CREATE (a)-[r:CONNECTED {
                from_device_id: $from_device_id,
                to_device_id: $to_device_id,
                method: $method,
                bluetooth_version: $bluetooth_version,
                signal_strength_dbm: $signal_strength_dbm,
                distance_meters: $distance_meters,
                duration_seconds: $duration_seconds,
                timestamp: $timestamp
            }]->(b)
            RETURN r
            """
            params = {
                "from_device_id": interaction.from_device,
                "to_device_id": interaction.to_device,
                "method": interaction.method,
                "bluetooth_version": interaction.bluetooth_version,
                "signal_strength_dbm": interaction.signal_strength_dbm,
                "distance_meters": interaction.distance_meters,
                "duration_seconds": interaction.duration_seconds,
                "timestamp": interaction.timestamp
            }

            result = session.run(query, params).data()
            return Success(result)
        except Exception as e:
            print(f"Error creating connection: {str(e)}")
            return Failure(str(e))

