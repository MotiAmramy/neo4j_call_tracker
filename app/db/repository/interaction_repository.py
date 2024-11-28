from returns.result import Success, Failure
from app.db.database import driver
from app.db.models.interaction import Interaction














def insert_interaction(interaction: Interaction):
    with driver.session() as session:
        try:
            query = """
            CREATE (inter:Interaction {
                from_device: $from_device, to_device: $to_device, method: $method, 
                bluetooth_version: $bluetooth_version, signal_strength_dbm: $signal_strength_dbm, 
                distance_meters: $distance_meters, duration_seconds: $duration_seconds, 
                timestamp: $timestamp})
            RETURN inter
            """

            # Convert timestamp to string if necessary (Neo4j typically stores date-time as strings or specific types)
            params = {
                "from_device": interaction.from_device,
                "to_device": interaction.to_device,
                "method": interaction.method,
                "bluetooth_version": interaction.bluetooth_version,
                "signal_strength_dbm": interaction.signal_strength_dbm,
                "distance_meters": interaction.distance_meters,
                "duration_seconds": interaction.duration_seconds,
                "timestamp": interaction.timestamp  # Convert timestamp to ISO string format
            }

            res = session.run(query, params).single()
            return Success(res['inter'])  # Return the inserted Interaction node

        except Exception as e:
            print(str(e))
            return Failure(str(e))