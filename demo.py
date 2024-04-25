# import psycopg2 as ps
# import numpy as np 
# import pandas as pd

# conn = ps.connect(database="postgres",user="postgres",password="Surendra@9144",host="localhost", port="5432")

# query = "select * from logistics_data"
# data=pd.read_sql(query,conn)
# print(data.head())

import re
p_num = re.compile(r'\d{3}-\d{3}-\d{4}')

num = p_num.search("i am surendra and my number is 914-914-4421")

print(num.group())



# from sklearn.impute import SimpleImputer
# from sklearn.pipeline import make_pipeline
# from sklearn.ensemble import GradientBoostingRegressor

# # Create a pipeline with an imputer
# pipeline = make_pipeline(SimpleImputer(strategy='mean'), GradientBoostingRegressor())

# # Fit the model
# pipeline.fit(X_train, y_train)

