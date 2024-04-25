#selecting the best model for prediction
def application():
    #importing necessary libraries
    import psycopg2 as pg
    import time
    import math
    import numpy as np
    import pandas as pd
    from feature_selection import features ,encoed_test,encoded_test_rem,fuel_charge
    from model_selection import split, mapped_cities
    from dist_calculation import haversine
    import streamlit as st
    import pickle
    from sklearn.preprocessing import LabelEncoder
    from discount import discount
    from table_update import update,update_data

    #creating a connection with the database
    conn = pg.connect(database="postgres",user="postgres",password="Surendra@9144",host="localhost", port="5432")


    #data selected for encoding
    query = "SELECT * FROM logistics_data"
    data = pd.read_sql(query, conn)



    # pd.set_option('display.max_columns',None)
    # print("data1")
    # print(data.head())


    #data selected for selecting the features
    # query_2 = "SELECT * FROM logistics_data"
    data_original = data.copy()
    # print("data2")
    # print(data_original.head())






    #data selected for encoding
    query_1 = "select * FROM cities_data"

    cities = pd.read_sql(query_1,conn)
    # print("data3")
    # print(cities.head())




    #data selected for selecting the features
    # query_3 = "select * FROM cities_data"
    # cities_original = pd.read_sql(query_3,conn)
    # print(cities_original.head()) 

    cities_original = cities.copy()
    # print("data4")
    # print(cities_original.head())


    #creating dictionry for mapping city with state
    mapped_cities_2 = mapped_cities(cities_original)







    #encoding the columns
    # col_to_encode_cities = ['city','state_id']
    # for col in col_to_encode_cities:
    #     # Initialize LabelEncoder
    #     label_encoder_cities = LabelEncoder()
    #     cities[col] = label_encoder_cities.fit_transform(cities[col])
    col_to_encode_cities = ['city', 'state_id']
    cities[col_to_encode_cities] = cities[col_to_encode_cities].apply(lambda x: LabelEncoder().fit_transform(x))


    # with open('label_encoder_cities.pkl', 'wb') as f:
    #     pickle.dump(label_encoder_cities, f)


    col_to_encode = ['origin_city','origin_state','destination_city','destination_state','equipment_type','rate_search_type']
    # for col in col_to_encode:
    #     label_encoder = LabelEncoder()
    #     data[col] = label_encoder.fit_transform(data[col])
    # col_to_encode = ['col1', 'col2', 'col3']  # Example list of columns to encode
    data[col_to_encode] = data[col_to_encode].apply(lambda x: LabelEncoder().fit_transform(x))


    # print(data.head())


    # with open('label_encoder.pkl', 'wb') as f:
    #     pickle.dump(label_encoder, f)



    #selecting the necessary features for trainin and evaluating the model
    data_to_predict = features(data)


    #this function is used to train and select the best model
    # model = split(data_to_predict)

    #create mapping between cities and states which are already encoded
    city_state_map = mapped_cities(cities)
    # print(city_state_map)

    #building the UI
    st.title('Flat Rate Prediction')
    columns = st.columns(2)
    with columns[0]:
        origin_city = st.selectbox('Select origin city:', options=list(mapped_cities_2.keys()))
        origin_state = mapped_cities_2[origin_city]
        st.selectbox('origin State', options=[origin_state])
    with columns[1]:
        dest_city = st.selectbox('Select destination city:', options=list(mapped_cities_2.keys()))
        dest_state = mapped_cities_2[dest_city]
        st.selectbox('Destination State', options=[dest_state])


    equipment_type = st.selectbox("Equipment Type", data_original['equipment_type'].unique(), index=0)
    rate_search_type = st.selectbox("Rate Search Type", data_original['rate_search_type'].unique(), index=0)
    vals = fuel_charge()
    fuel_cost = st.write("fuel cost is ",round(vals),"dollars")
    date = st.date_input("Date")
    #encoding the origin and destination values
    en_origin_city,en_origin_state,en_dest_city,en_dest_state = encoed_test(origin_city,origin_state,dest_city,dest_state)


    #encoding truck type and rate search type
    en_equipment_type,en_rate_search_type = encoded_test_rem(equipment_type,rate_search_type)






    if st.button("Predict"):
        try:
            #this function is used to train and select the best model
            model = split(data_to_predict)
            year, month, day = date.year, date.month, date.day
            origin_coords = (cities_original.loc[(cities_original['city'] == origin_city) & (cities_original['state_id'] == origin_state), 'lat'].iloc[0], cities_original.loc[(cities_original['city'] == origin_city) & (cities_original['state_id'] == origin_state), 'lng'].iloc[0])
            destination_coords = (cities_original.loc[(cities_original['city'] == dest_city) & (cities_original['state_id'] == dest_state), 'lat'].iloc[0], cities_original.loc[(cities_original['city'] == dest_city) & (cities_original['state_id'] == dest_state), 'lng'].iloc[0])
            avg_distance = haversine(*origin_coords, *destination_coords)
            st.write("the distance is {}".format(round(avg_distance)))
            avg_rate_per_mile = model.predict([[en_origin_city,en_origin_state,en_dest_city,en_dest_state, en_equipment_type,en_rate_search_type,fuel_cost, year, month, day]])
            miles_rate = avg_rate_per_mile.item()
            st.write("Rate per mile is",avg_rate_per_mile)
            total = math.ceil(avg_distance*avg_rate_per_mile)
            st.write("total cost before discount is ",total)
            d_total = math.ceil(discount(avg_distance,avg_rate_per_mile))
            st.write("total cost after discount is ",d_total)

            # o_lat,o_lon,d_lat,d_lon = update(conn,origin_city,origin_state,dest_state,dest_city)
            o_lat,o_lon = origin_coords
            d_lat,d_lon = destination_coords

            update_data(conn,origin_city,origin_state,o_lat,o_lon,dest_city,dest_state,d_lat,d_lon,equipment_type,rate_search_type,vals,miles_rate, year, month, day)


            


            
        except ValueError as e:
            st.error("An error occurred: {}".format(e))



