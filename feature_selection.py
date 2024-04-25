# feature selection and encoding categorical features
import psycopg2 as pg
import pandas as pd
import random

conn1 = pg.connect(database="postgres",user="postgres",password="Surendra@9144",host="localhost", port="5432")

query_1 = "select * FROM cities_data"

cities = pd.read_sql(query_1,conn1)

# print(cities['city'].unique())
# print(cities['state_id'].unique())



#retreving necessary rows which are used for prediction
def features(data_set):
    new_data=data_set[['origin_city', 'origin_state','destination_city', 'destination_state', 'equipment_type', 'rate_search_type','fuel_charges', 'date_year', 'date_month', 'data_date','avg_rate_rpm']]
    print(new_data.head())
    return new_data


#generating a random value as fuel charge
def fuel_charge():
    return random.uniform(3, 5)


#encoding the values
def encoed_test(origin_city, origin_state, dest_city, dest_state):
    from sklearn.preprocessing import OneHotEncoder

    # Combine the city and state values into a 2D array-like structure
    cities_states = [[origin_city, origin_state], [dest_city, dest_state]]

    # Initialize the OneHotEncoder
    encoder = OneHotEncoder()

    # Fit and transform the combined city and state values
    encoded_data = encoder.fit_transform(cities_states)

    # Separate the encoded values back into individual variables
    en_origin_city, en_origin_state, en_dest_city, en_dest_state = encoded_data[0, 0], encoded_data[0, 1], encoded_data[1, 0], encoded_data[1, 1]

    return en_origin_city, en_origin_state, en_dest_city, en_dest_state



def encoded_test_rem(equipment_type, rate_search_type):
    from sklearn.preprocessing import OneHotEncoder
    encoded_test_col = [[equipment_type, rate_search_type]]
    encoder = OneHotEncoder()
    
    encoded_test_col = encoder.fit_transform(encoded_test_col)
    en_equipment_type, en_rate_search_type = encoded_test_col[0, 0],encoded_test_col[0,1]
    
    return en_equipment_type, en_rate_search_type



















































































































# import psycopg2 as pg
# import pandas as pd
# import pickle

# # Establish database connection
# conn1 = pg.connect(database="postgres", user="postgres", password="Surendra@9144", host="localhost", port="5432")

# # Query cities data
# query_1 = "select * FROM cities_data"
# cities = pd.read_sql(query_1, conn1)

# # Function to select specific columns from a dataset
# def features(data_set):
#     new_data = data_set[['origin_city', 'origin_state', 'destination_city', 'destination_state', 'equipment_type', 'rate_search_type', 'fuel_charges', 'date_year', 'date_month', 'data_date', 'avg_rate_rpm']]
#     return new_data

# # Function to encode city and state values
# def encoed_test(origin_city, origin_state, dest_city, dest_state):
#     with open('label_encoder_cities.pkl', 'rb') as f:
#         label_encoder_cities = pickle.load(f)

#     encoded_data = {}
#     for col in ['origin_city', 'origin_state', 'destination_city', 'destination_state']:
#         if col == 'origin_city':
#             col_val = origin_city
#         elif col == 'origin_state':
#             col_val = origin_state
#         elif col == 'destination_city':
#             col_val = dest_city
#         else:
#             col_val = dest_state

#         if col_val not in label_encoder_cities.classes_:
#             # Handle unseen labels
#             # You can choose to ignore them, assign a default value, or encode them as a special category
#             # For now, let's encode them as a special category (e.g., -1)
#             encoded_data[col] = -1
#         else:
#             encoded_data[col] = label_encoder_cities.transform([col_val])[0]

#     return encoded_data['origin_city'], encoded_data['origin_state'], encoded_data['destination_city'], encoded_data['destination_state']

# # Example usage
# en_origin_city, en_origin_state, en_dest_city, en_dest_state = encoed_test('New York', 'NY', 'Los Angeles', 'CA')
# print(en_origin_city, en_origin_state, en_dest_city, en_dest_state)


# with open('label_encoder_cities.pkl', 'rb') as f:
    #     label_encoder_cities = pickle.load(f)
    #     encoded_data = {}
    #     for col in encoded_col:
    #         # encoded_data[col] = label_encoder_cities.transform([col])[0]
    #         encoded_data[col] = label_encoder_cities.transform(cities[col])[0]
