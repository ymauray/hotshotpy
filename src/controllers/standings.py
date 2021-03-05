import hotshotpy


def get(query_string):
    event_id = query_string['event_id'][0]
    conn = hotshotpy.create_connection()
    c = conn.cursor()
    sql = f"""SELECT DISTINCT r.driver_id, d.name, d.flag FROM results r, drivers d WHERE r.event_id = {event_id} AND d.id = r.driver_id;"""
    c.execute(sql)
    driver_rows = c.fetchall()
    c.close()

    c = conn.cursor()
    sql = f"""SELECT DISTINCT r.race_id FROM results r WHERE r.event_id = {event_id};"""
    c.execute(sql)
    races_rows = c.fetchall()
    c.close()

    c = conn.cursor()
    sql = f"""SELECT id, race_id, pos, driver_id, race_time FROM results WHERE event_id = {event_id};"""
    c.execute(sql)
    results_rows = c.fetchall()
    c.close()

    c = conn.cursor()
    sql = f"""SELECT id, name FROM events WHERE id = {event_id};"""
    c.execute(sql)
    event_row = c.fetchone()
    c.close()

    return {
        "event_name": event_row['name'],
        "event_id": event_row['id'],
        "race_count": len(races_rows),
        "drivers": [{
            "name": driver_row['name'],
            "id": driver_row['driver_id'],
            "flag": driver_row['flag'],
            "points": 0,
            "finishes": []
        } for driver_row in driver_rows],
        "races": [race_row['race_id'] for race_row in races_rows],
    }
