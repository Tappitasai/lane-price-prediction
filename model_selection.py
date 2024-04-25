#machine learning  model
def split(data):
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_squared_error
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import make_pipeline
    x=data.drop(columns=["avg_rate_rpm"],axis=1)
    y=data["avg_rate_rpm"]
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

    models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(),
    'Lasso Regression': Lasso(),
    'ElasticNet': ElasticNet(),
    'Decision Tree Regressor': DecisionTreeRegressor(),
    'Random Forest Regressor': RandomForestRegressor(),
    'AdaBoost Regressor': AdaBoostRegressor(),
    'SVR': SVR(),
    'KNN Regressor': KNeighborsRegressor(),
    'MLP Regressor': MLPRegressor()
    }

    param_grid = {
    'Linear Regression': {},
    'Ridge Regression': {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0], 'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']},
    'Lasso Regression': {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0]},
    'ElasticNet': {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0], 'l1_ratio': [0.1, 0.5, 0.9]},
    'Decision Tree Regressor': {'max_depth': [None, 10, 20, 30, 40, 50], 'min_samples_split': [2, 5, 10]},
    'Random Forest Regressor': {'n_estimators': [100, 200, 300], 'max_depth': [None, 10, 20, 30, 40, 50], 'min_samples_split': [2, 5, 10]},
    'AdaBoost Regressor': {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.5]},
    'SVR': {'kernel': ['linear', 'poly', 'rbf'], 'C': [0.1, 1, 10]},
    'KNN Regressor': {'n_neighbors': [3, 5, 7, 9]},
    'MLP Regressor': {'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 100)], 'activation': ['relu', 'tanh', 'logistic']}
    }
    best_model_last = None
    best_mse = float('inf')
    # Perform GridSearchCV for each model
    for name, model in models.items():
        print(f"Performing GridSearchCV for {name}...")
        grid_search = GridSearchCV(model, param_grid[name], cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(x_train, y_train)
        
        # Get the best hyperparameters
        best_params = grid_search.best_params_
        print(f"Best Hyperparameters for {name}:", best_params)
        
        # Use the best hyperparameters to train the final model
        best_model = model.__class__(**best_params)
        best_model.fit(x_train, y_train)
        y_pred = best_model.predict(x_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"{name} MSE with Best Hyperparameters:", mse)
        print()

        if mse < best_mse:
            best_model_last = best_model
            best_mse=mse
    print("best model is {} with mse {}".format(best_model_last,best_mse))
    return best_model_last


#creating mapping between cities and states 
def mapped_cities(data):
    cities = data["city"].tolist()
    states_id = data["state_id"].tolist()
    city_state_map = dict(zip(cities, states_id))
    return city_state_map
