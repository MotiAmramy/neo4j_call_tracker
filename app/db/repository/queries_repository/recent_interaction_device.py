from app.db.database import driver



def get_most_recent_interaction(device_id):
    try:
        with driver.session() as session:
            query = """
            MATCH (a:Device)-[r:CONNECTED]->(b:Device)
            WHERE a.id = $device_id
            RETURN r.timestamp AS interaction_timestamp, r.method AS connection_method, 
                   r.signal_strength_dbm AS signal_strength, r.distance_meters AS distance
            ORDER BY r.timestamp DESC
            LIMIT 1
            """
            result = session.run(query, {"device_id": device_id})
            record = result.single()
            return {
                "interaction_timestamp": record["interaction_timestamp"],
                "connection_method": record["connection_method"],
                "signal_strength_dbm": record["signal_strength"],
                "distance_meters": record["distance"]
            }
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}