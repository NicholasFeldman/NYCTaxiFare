import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

print("Reading Training Data...")
training_data = pd.read_csv('train.csv')

print("Reading Testing Data...")
test_data = pd.read_csv('test.csv')


def add_year_month_hour_to_data(data):
    data['tpep_pickup_datetime'] = data['tpep_pickup_datetime'].str.slice(0, 16)
    data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'], utc=True, format='%Y-%m-%d %H:%M')
    data['year'] = pd.DatetimeIndex(data['tpep_pickup_datetime']).year
    data['month'] = pd.DatetimeIndex(data['tpep_pickup_datetime']).month
    data['hour'] = pd.DatetimeIndex(data['tpep_pickup_datetime']).hour
    return data


print("Adding Year, Month, and Hour to Training Data...")
training_data = add_year_month_hour_to_data(training_data)

print("Adding Year, Month, and Hour to Testing Data...")
test_data = add_year_month_hour_to_data(test_data)


def create_column_stack(df):
    return np.column_stack((df.year, df.month, df.hour, df.PULocationID, df.DOLocationID))


training_stack = create_column_stack(training_data)
training_array = np.array(training_data['fare_amount'])

print("Performing Random Forest Regression...")
regression = RandomForestRegressor(n_estimators=30, max_depth=20, random_state=0, n_jobs=-1, verbose=2)
regression.fit(training_stack, training_array)

testing_stack = create_column_stack(test_data)
test_prediction = regression.predict(testing_stack)

print("Creating Data Frame...")
submission = pd.DataFrame({
    'PULocationID': test_data.PULocationID,
    'DOLocationID': test_data.DOLocationID,
    'fare_amount': test_prediction
}, columns=['PULocationID', 'DOLocationID', 'fare_amount'])

print("Writing Output to output.csv...")
submission.to_csv('output.csv', index=False)
