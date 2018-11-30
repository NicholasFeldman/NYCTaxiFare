import os
import glob
import pandas as pd
from datetime import datetime

PU_DATETIME = 1
PASSENGER_COUNT = 3
PU_LOCATION = 7
DO_LOCATION = 8
TOTAL = 10
DATA_TO_KEEP = [PASSENGER_COUNT, PU_LOCATION, DO_LOCATION, TOTAL]
CSV_HEADERS = ','.join(['passenger_count', 'PULocationID', 'DOLocationID', 'fare_amount', 'year', 'month', 'hour'])

def write_headers(file_path):
    with open(file_path, 'w') as write_file:
        write_file.write(CSV_HEADERS + '\n')

def datetime_to_data(date):
    date_info = datetime.strptime(date[:16], '%Y-%m-%d %H:%M')
    return [str(date_info.year), str(date_info.month), str(date_info.hour)]

def process_data(line):
    data = line.split(',')
    if line == '' or data[0] == 'VendorID':
        return None
    processed_data = [data[i] for i in DATA_TO_KEEP] + datetime_to_data(data[PU_DATETIME])
    return ','.join(processed_data)

def main():
    count = 0
    train_path = os.path.join(os.getcwd() + '/output/', 'train.csv')
    test_path = os.path.join(os.getcwd() + '/output/', 'test.csv')
    write_headers(train_path)
    write_headers(test_path)
    for filename in glob.glob(os.path.join(os.getcwd() + '/input', '*.csv')):
        print('reading: ' + filename)
        for line in open(filename, 'r'):
            processed_data = process_data(line.strip())
            if processed_data == None:
                continue
            if count == 3:
                with open(test_path, 'a') as test_file:
                    test_file.write(processed_data + '\n')
                count = 0
            else:
                count += 1
                with open(train_path, 'a') as train_file:
                    train_file.write(processed_data + '\n')

main()
