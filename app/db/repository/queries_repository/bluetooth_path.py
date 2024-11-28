from app.db.database import driver


def find_bluetooth_connected_devices():
    try:
        with driver.session() as session:

            query = """
            MATCH (start:Device) MATCH (end:Device)
            WHERE start <> end
            MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
            WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
            WITH path, length(path) AS pathLength
            ORDER BY pathLength DESC LIMIT 1 RETURN path
            """
            result = session.run(query)
            paths_data = [
                {
                    "devices": [
                        {"id": node["id"], "name": node["name"], "brand": node["brand"], "model": node["model"], "os": node["os"]}
                        for node in record["path"].nodes
                    ],
                    "path_length": len(record["path"].relationships)
                }
                for record in result
            ]
            return paths_data

    except Exception as e:
        return {"error": "Database Error", "details": str(e)}