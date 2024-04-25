import streamlit as st
from model_selection import mapped_cities


# city_state_map = mapped_cities(cities)

st.title('Flat Rate Prediction')
columns = st.columns(2)
with columns[0]:
    origin_city = st.selectbox('Select origin city:', options=list(city_state_map.keys()))
    origin_state=city_state_map[origin_city]
    st.selectbox('origin State', options=[origin_state])
with columns[1]:
    dest_city = st.selectbox('Select destination city:', options=list(city_state_map.keys()))
    dest_state = city_state_map[dest_city]
    st.selectbox('Destination State', options=[dest_state])

equipment_type = st.selectbox("Equipment Type", Data['equipment_type'].unique(), index=0)
rate_search_type = st.selectbox("Rate Search Type", Data['rate_search_type'].unique(), index=0)
date = st.date_input("Date")




if st.button("Predict"):
    try:
        year, month, day = date.year, date.month, date.day
        origin_coords = (capitals.loc[(capitals['city'] == origin_city) & (capitals['state_id'] == origin_state), 'lat'].iloc[0], capitals.loc[(capitals['city'] == origin_city) & (capitals['state_id'] == origin_state), 'lng'].iloc[0])
        destination_coords = (capitals.loc[(capitals['city'] == dest_city) & (capitals['state_id'] == dest_state), 'lat'].iloc[0], capitals.loc[(capitals['city'] == dest_city) & (capitals['state_id'] == dest_state), 'lng'].iloc[0])

        avg_distance = haversine(*origin_coords, *destination_coords)
        # result = encode_lat(origin_coords, destination_coords)
        # o_lat, o_lng = result[0]
        # d_lat, d_lng = result[1]

        # avg_rate_rpm = model.predict([[o_lat, o_lng, d_lat, d_lng, equipment_type,1,0 ,avg_distance, rate_search_type, year, month, day]])

        st.write("the average prm is {}".format(avg_rate_rpm))
