import numpy as np
import pandas as pd
import datetime
from sklearn.ensemble import RandomForestRegressor
from google.cloud import storage
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline

bucket = storage.Client("cloudcomputing-222017").bucket('cloud-computing-input')

blob1 = bucket.blob('yellow_tripdata_2017-03.csv')

blob1.download_to_filename('test.csv')

blob2 = bucket.blob('yellow_tripdata_2017-04.csv')

blob2.download_to_filename('train.csv')

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


# Export the model to a file
pipeline = Pipeline([
    ('classifier', regression)
])

model = 'model.joblib'
joblib.dump(pipeline, model)

# Upload the model to GCS
bucket = storage.Client("cloudcomputing-222017").bucket('cloud-computing-model-code')
blob = bucket.blob('{}/{}'.format(
    datetime.datetime.now().strftime('Taxi_%Y%m%d_%H%M%S'),
    model))
blob.upload_from_filename(model)
