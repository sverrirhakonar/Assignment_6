import csv  
import os   
from models import Stock, Bond, ETF, MarketDataPoint
import pandas as pd
from patterns.singleton import Config 
from patterns.factory import InstrumentFactory
from data_loader import YahooFinanceAdapter, BloombergXMLAdapter
from engine import TradingEngine
from patterns.strategy import MeanReversionStrategy, BreakoutStrategy
from reporting import LoggerObserver, AlertObserver 
from datetime import datetime

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

    # --- Test Instrument Loading (Task 1) ---
    print("--- Testing Instrument Loading ---")
    list_of_instruments = get_instruments(INSTRUMENT_FILE)
    if list_of_instruments:
        print(f"Loaded {len(list_of_instruments)} instruments.")
    else:
        print("No instruments loaded.")
    print("--------------------------------")

    # --- Test Singleton Config (Task 2) ---
    print("\n--- Testing Singleton Config ---")
    config1 = Config(CONFIG_FILE, PARAMS_FILE)
    config2 = Config()
    print(f"Config is Singleton: {config1 is config2}")
    print(f"Log Level from Config: {config1.get_setting('log_level', 'DEFAULT')}")
    print(f"MA Window from Config: {config1.get_setting('strategy_params.MeanReversionStrategy.lookback_window', 'DEFAULT')}")
    print("----------------------------")

    # --- Test Adapters (Task 4) ---
    print("\n--- Testing Adapters ---")
    yahoo_adapter = YahooFinanceAdapter(YAHOO_DATA_FILE)
    aapl_data_yahoo = yahoo_adapter.get_data('AAPL')
    if aapl_data_yahoo: print(f"Yahoo AAPL Data: {aapl_data_yahoo}")
    
    bloomberg_adapter = BloombergXMLAdapter(BLOOMBERG_DATA_FILE)
    msft_data_bloomberg = bloomberg_adapter.get_data('MSFT')
    if msft_data_bloomberg: print(f"Bloomberg MSFT Data: {msft_data_bloomberg}")
    print("----------------------")

    # --- Test Strategy Engine with Observers (Task 5 & 6) ---
    print("\n--- Testing Strategy Engine (Mean Reversion) ---")
    
    # 1. Create strategy
    mean_rev_strategy = MeanReversionStrategy()
    
    # 2. Create engine
    engine = TradingEngine(mean_rev_strategy)

    # 3. Create observers
    logger = LoggerObserver()
    alerter = AlertObserver()

    # 4. ATTACH observers to the engine
    print("Attaching observers...")
    engine.attach(logger)
    engine.attach(alerter)

    # 5. Create mock data (using a list with known triggers)
    mock_feed_mr = [
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 30, 0), symbol='AAPL', price=100.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 31, 0), symbol='AAPL', price=101.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 32, 0), symbol='AAPL', price=102.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 33, 0), symbol='AAPL', price=101.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 34, 0), symbol='AAPL', price=100.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 35, 0), symbol='AAPL', price=80.0),  # Should trigger BUY
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 36, 0), symbol='AAPL', price=120.0)  # Should trigger SELL
    ]

    # 6. Run the engine
    # Now, when run() finds a signal, it will call publisher.notify(),
    # which will call update() on both 'logger' and 'alerter'.
    engine.run(mock_feed_mr)
    
    print("\n--- Testing Strategy Engine (Breakout) ---")
    # 1. Create strategy
    breakout_strategy = BreakoutStrategy()
    
    # 2. Create engine
    engine2 = TradingEngine(breakout_strategy)
    
    # 3. ATTACH observers (we can reuse the same logger/alerter objects)
    print("Attaching observers...")
    engine2.attach(logger)
    engine2.attach(alerter)
    
    # You can also detach an observer if needed
    # engine2.detach(alerter) 

    # 4. Create mock data
    mock_feed_bo = [
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 30, 0), symbol='MSFT', price=200.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 31, 0), symbol='MSFT', price=201.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 32, 0), symbol='MSFT', price=200.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 33, 0), symbol='MSFT', price=201.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 34, 0), symbol='MSFT', price=205.0), # Should trigger BUY
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 35, 0), symbol='MSFT', price=195.0)  # Should trigger SELL
    ]
    
    # 5. Run the second engine
    engine2.run(mock_feed_bo)
    print("---------------------------------")





