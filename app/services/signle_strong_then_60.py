from app.db.database import driver


def get_strong_device_connections():
    with driver.session() as session:
        try:
            # Cypher query to find devices connected with signal strength > -60 dBm
            query = """
            MATCH (a:Device)-[r:CONNECTED]->(b:Device)
            WHERE r.signal_strength_dbm > -60
            RETURN DISTINCT a, b
            """

            # Execute the query
            result = session.run(query)

            # Extracting the device details from the result
            devices_data = [
                {
                    'from_device': {
                        'id': record['a']['id'],
                        'name': record['a']['name'],
                        'brand': record['a']['brand'],
                        'model': record['a']['model'],
                        'os': record['a']['os']
                    },
                    'to_device': {
                        'id': record['b']['id'],
                        'name': record['b']['name'],
                        'brand': record['b']['brand'],
                        'model': record['b']['model'],
                        'os': record['b']['os']
                    }
                }
                for record in result
            ]

            return devices_data
        except Exception as e:
            return {"error": "Database Error", "details": str(e)}