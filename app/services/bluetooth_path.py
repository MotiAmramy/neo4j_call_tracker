from app.db.database import driver


def find_bluetooth_connected_devices():
    try:
        with driver.session() as session:

            query = """
            MATCH path = (a:Device)-[r:CONNECTED*]->(b:Device)
            WHERE ALL(rel IN relationships(path) WHERE rel.method = 'Bluetooth')
            RETURN [node IN nodes(path) | {id: node.id, name: node.name, brand: node.brand, model: node.model, os: node.os}] AS devices,
                   length(path) AS path_length
            """

            return [
                {"devices": record["devices"], "path_length": record["path_length"]}
                for record in session.run(query)
            ]
    except Exception as e:
        return {"error": "Database Error", "details": str(e)}