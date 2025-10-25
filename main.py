
import csv  
import os   
from models import Stock, Bond, ETF 
import pandas as pd


INSTRUMENT_PATH = 'data/instruments.csv'


def get_instruments(csv_path):
    instruments = []
    with open(csv_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Example: check 'type' column and do something
            if row['type'] == 'Stock':
                instruments.append(Stock(row['symbol'], float(row['price']), row['issuer'], row['sector']))
            elif row['type'] == 'Bond':
                # Do something with bond
                instruments.append(Bond(row['symbol'], float(row['price']), row['issuer'], row['sector'], row['maturity']))
            elif row['type'] == 'ETF':
                instruments.append(ETF(row['symbol'], float(row['price']), row['issuer'], row['sector']))
            else:
                # Error handling
                print('bro not correct type')
    return instruments

list_of_instruments = get_instruments(INSTRUMENT_PATH)
