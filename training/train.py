import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import mlflow
import mlflow.sklearn
import numpy as np



df = pd.read_csv("data/housing_clean.csv")

X = df.drop(columns=["median_house_value"])
y = df["median_house_value"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("CaliforniaHousingPrediction")

with mlflow.start_run():
    model = LinearRegression()
    model.fit(X_train, y_train)

    #Predictions
    y_pred = model.predict(X_test)

    #Metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))  
    mae = mean_absolute_error(y_test, y_pred)

    #Logging
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)

    #Saving the model
    input_example = X_test.iloc[0:1]  
    mlflow.sklearn.log_model(model, "model", input_example=input_example)