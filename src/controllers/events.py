from threading import current_thread
from database import create_connection, execute_sql


def get(query_string):
    conn = create_connection()

    c = conn.cursor()

    sql = """select current_event_id from params;"""

    c.execute(sql)

    rows = c.fetchall()

    current_event_id = rows[0][0]

    c.close()

    c = conn.cursor()

    sql = """select * from events order by id desc;"""

    c.execute(sql)

    rows = c.fetchall()

    c.close()

    events = []

    for row in rows:
        event = dict()
        for key in row.keys():
            event[key] = row[key]
        events.append(event)

    return {
        "current_event_id": current_event_id,
        "events": events
    }


def set_current(query_string):
    current_event_id = query_string['current'][0]
    conn = create_connection()
    sql = f"""update params set current_event_id = {current_event_id};"""
    execute_sql(conn, sql)
    conn.commit()
    conn.close()
