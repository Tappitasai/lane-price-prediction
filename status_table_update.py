#code for updating the table used for storing the logs
from app import application
import psycopg2 as pg
import pandas as pd
from datetime import datetime
import time

conn = pg.connect(database="postgres", user="postgres", password="Surendra@9144", host="localhost", port="5432")


def status_update(conn):
    # Query to get the previous count
    query_1 = "SELECT no_of_rows FROM status WHERE modified_time = (SELECT MAX(modified_time) FROM status)"
    prev_count_df = pd.read_sql(query_1, conn)

    # If there are no previous counts, set prev_count to 0
    prev_count = prev_count_df['no_of_rows'].values[0] if not prev_count_df.empty else 0

    # Query to get the current count
    query_2 = "SELECT COUNT(*) FROM logistics_data"
    current_count_df = pd.read_sql(query_2, conn)
    current_count = current_count_df['count'].values[0]
    print(current_count, prev_count)

    # Compare the counts and update if necessary
    if prev_count < current_count:
        query_3 = "INSERT INTO status (no_of_rows, modified_time) VALUES (%s, %s)"
        values = (int(current_count), datetime.now())
        cursor = conn.cursor()
        cursor.execute(query_3, values)
        conn.commit()


# status_update(conn)

# delay = 43200

# while True:
#     time.sleep(delay)

application()
status_update(conn)
