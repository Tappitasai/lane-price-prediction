# import psycopg2 as pg
import pandas as pd
# conn = pg.connect(database="postgres",user="postgres",password="Surendra@9144",host="localhost", port="5432")

def update_data(conn,o_city,o_state,o_lat,o_lon,d_city,d_state,d_lat,d_lon,e_type,r_type,fuel,rmp,year,month,day):
    # print("o_city:", type(o_city).__name__)
    # print("o_state:", type(o_state).__name__)
    # print("o_lat:", type(o_lat).__name__)
    # print("o_lon:", type(o_lon).__name__)
    # print("d_city:", type(d_city).__name__)
    # print("d_state:", type(d_state).__name__)
    # print("d_lat:", type(d_lat).__name__)
    # print("d_lon:", type(d_lon).__name__)
    # print("e_type:", type(e_type).__name__)
    # print("r_type:", type(r_type).__name__)
    # print("fuel:", type(fuel).__name__)
    # print("rmp:", type(rmp).__name__)
    # print("year:", type(year).__name__)
    # print("month:", type(month).__name__)
    # print("day:", type(day).__name__)
    # # Create a cursor object
    cur = conn.cursor()

    # Check if the data already exists
    cur.execute(
        "SELECT * FROM logistics_data WHERE origin_city = %s AND origin_state = %s AND origin_latitude = %s AND origin_longitude = %s AND destination_city = %s AND destination_state = %s AND dest_latitude = %s AND dest_longitude = %s AND equipment_type = %s AND rate_search_type = %s AND fuel_charges = %s and avg_rate_rpm = %s And date_year = %s AND date_month = %s AND data_date = %s",
        (o_city,o_state,o_lat,o_lon,d_city,d_state,d_lat,d_lon,e_type,r_type,fuel,rmp,year,month,day)
    )

#     cur.execute(
#         "SELECT * FROM logistics_data WHERE o_city = %s AND o_state = %s AND o_lat = %s AND o_lon = %s AND d_city = %s AND d_state = %s AND d_lat = %s AND d_lon = %s AND e_type = %s AND r_type = %s AND fuel = %s AND rmp = %s AND year = %s AND month = %s AND day = %s",
#     (o_city, o_state, o_lat, o_lon, d_city, d_state, d_lat, d_lon, equipment_type, rate_search_type, val, avg_rate_per_mile, year, month, day)
# )


    existing_data = cur.fetchone()

    # If data doesn't exist, insert it into the table
    if not existing_data:
        cur.execute(
            "INSERT INTO logistics_data (origin_city, origin_state, origin_latitude, origin_longitude,destination_city, destination_state, dest_latitude,dest_longitude, equipment_type, rate_search_type, fuel_charges,avg_rate_rpm, date_year, date_month, data_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)",
            (o_city,o_state,o_lat,o_lon,d_city,d_state,d_lat,d_lon,e_type,r_type,fuel,rmp,year,month,day)
        )


        # cur.execute( 
        #     "INSERT INTO STATUS (no_of_rows,modified_time) VALUES (%s,%s) ",
        #     WHERE no_of_row
        # )

        # cur.execute(
        #     "INSERT INTO logistics_data (o_city,o_state,o_lat,o_lon,d_city,d_state,d_lat,d_lon,e_type,r_type,fuel,rmp,year,month,day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)",
        #     (origin_city, origin_state, origin_latitude, origin_longitude,destination_city, destination_state, dest_latitude,dest_longitude, equipment_type, rate_search_type, fuel_charges,avg_rate_rpm, date_year, date_month, data_date))


        conn.commit()
        print("Data inserted successfully.")
    else:
        print("data is not inserted as it already exist")



def update(conn,o_city,o_state,d_city,d_state):
    query = "SELECT * from cities_data"
    cities = pd.read_sql(query,conn)
    origin_lat,origin_lon = (cities.loc[(cities['city'] == o_city) & (cities['state_id'] == o_state), 'lat'].iloc[0], cities.loc[(cities['city'] == o_city) & (cities['state_id'] == o_state), 'lng'].iloc[0])
    destination_lat,destination_lon = (cities.loc[(cities['city'] == d_city) & (cities['state_id'] == d_state), 'lat'].iloc[0], cities.loc[(cities['city'] == d_city) & (cities['state_id'] == d_state), 'lng'].iloc[0])
    # print(origin_lat,origin_lon,destination_lat,destination_lon)
    return origin_lat,origin_lon,destination_lat,destination_lon



        
    
    


