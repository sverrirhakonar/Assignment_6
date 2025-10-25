
import csv  
import os   
from models import Stock, Bond, ETF 
import pandas as pd
from patterns.singleton import Config 

INSTRUMENT_FILE = os.path.join('data', 'instruments.csv')
CONFIG_FILE = os.path.join('data', 'config.json')
PARAMS_FILE = os.path.join('data', 'strategy_params.json')

def get_instruments(csv_path):
    instruments = []
    with open(csv_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['type'] == 'Stock':
                instruments.append(Stock(row['symbol'], float(row['price']), row['issuer'], row['sector']))
            elif row['type'] == 'Bond':
                instruments.append(Bond(row['symbol'], float(row['price']), row['issuer'], row['sector'], row['maturity']))
            elif row['type'] == 'ETF':
                instruments.append(ETF(row['symbol'], float(row['price']), row['issuer'], row['sector']))
            else:
                # Error handling
                print('bro not correct type')
    return instruments


if __name__ == "__main__":

    print("--- Getting Config Instance (First Time) ---")
    config_manager = Config(CONFIG_FILE, PARAMS_FILE)
    print(f"\nLoading instruments from: {CONFIG_FILE}") # Using config might be better later
    list_of_instruments = get_instruments(INSTRUMENT_FILE) # Example using config for path
    print("\n--- Accessing Config Settings ---")
    # Get the instance again (note: no file paths needed now)
    config_again = Config()
    print(f"Is it the same config object? {config_manager is config_again}")
    # Use get_setting to access configuration values
    log_level = config_manager.get_setting('logging.level', 'INFO') # Example top-level key
    print(f"Logging level from config: {log_level}")
    # Example accessing nested strategy params using dot notation
    ma_window = config_manager.get_setting('strategy_params.MeanReversionStrategy.window', 30)
    print(f"MA Strategy Window from config: {ma_window}")
    # Example accessing a setting that might not exist, using default
    broker_url = config_manager.get_setting('broker.url', 'http://default-broker.com')
    print(f"Broker URL: {broker_url}")
    print("---------------------------------")

