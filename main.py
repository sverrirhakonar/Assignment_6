import csv  
import os   
from models import Stock, Bond, ETF, MarketDataPoint
import pandas as pd
from patterns.singleton import Config 
from patterns.factory import InstrumentFactory
from data_loader import YahooFinanceAdapter, BloombergXMLAdapter

INSTRUMENT_FILE = os.path.join('data', 'instruments.csv')
CONFIG_FILE = os.path.join('data', 'config.json')
PARAMS_FILE = os.path.join('data', 'strategy_params.json')
YAHOO_DATA_FILE = os.path.join('data', 'external_data_yahoo.json') 
BLOOMBERG_DATA_FILE = os.path.join('data', 'external_data_bloomberg.xml')

def get_instruments(csv_path):
    instruments = []
    with open(csv_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instrument = InstrumentFactory.create_instrument(row)
            if instrument:
                instruments.append(instrument)
    return instruments


# --- Main execution block ---
if __name__ == "__main__":

    # --- Test Instrument Loading ---
    print("--- Testing Instrument Loading ---")
    list_of_instruments = get_instruments(INSTRUMENT_FILE)
    if list_of_instruments:
        print(f"Loaded {len(list_of_instruments)} instruments.")
    else:
        print("No instruments loaded.")
    print("--------------------------------")

    # --- Test Singleton Config ---
    print("\n--- Testing Singleton Config ---")
    # First call initializes
    config1 = Config(CONFIG_FILE, PARAMS_FILE)
    # Second call gets the same instance
    config2 = Config()

    print(f"Config is Singleton: {config1 is config2}") # Verify same object
    # Access a setting to check loading
    print(f"Log Level from Config: {config1.get_setting('log_level', 'DEFAULT')}")
    print(f"MA Window from Config: {config1.get_setting('strategy_params.MeanReversionStrategy.lookback_window', 'DEFAULT')}")
    print("----------------------------")

# --- Test YahooFinanceAdapter ---  # <-- New Test Block
    print("\n--- Testing Yahoo Adapter ---")
    yahoo_adapter = YahooFinanceAdapter(YAHOO_DATA_FILE)
    aapl_data = yahoo_adapter.get_data('AAPL') # Try getting data for AAPL
    if aapl_data:
        print(f"Yahoo AAPL Data: {aapl_data}") # Relies on MarketDataPoint.__repr__
    else:
        print("Could not retrieve AAPL data from Yahoo adapter.")
    print("---------------------------")

# --- Test BloombergXMLAdapter ---  # <-- New Test Block
    print("\n--- Testing Bloomberg Adapter ---")
    bloomberg_adapter = BloombergXMLAdapter(BLOOMBERG_DATA_FILE)
    msft_data_bloomberg = bloomberg_adapter.get_data('MSFT') # Try getting data for MSFT
    if msft_data_bloomberg:
        print(f"Bloomberg MSFT Data: {msft_data_bloomberg}") # Relies on MarketDataPoint.__repr__
    else:
        print("Could not retrieve MSFT data from Bloomberg adapter.")
    print("-------------------------------")
