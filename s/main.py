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
from reporting import LoggerObserver, AlertObserver, OrderObserver 
from portfolio import Portfolio 
from patterns.command import CommandInvoker

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
    # (Update your strategy params json to 5 and 4 for this test to work!)
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

    # --- Setup for Task 6 & 7: Portfolio, Invoker, Observers ---
    print("\n--- Initializing Portfolio, Invoker, and Observers ---")
    
    # 1. Create the Receiver
    portfolio = Portfolio(initial_cash=500_000.0)
    
    # 2. Create the Invoker
    invoker = CommandInvoker()
    
    # 3. Create Observers
    logger = LoggerObserver()
    alerter = AlertObserver()
    # Create the new OrderObserver, giving it the portfolio and invoker
    order_executor = OrderObserver(portfolio=portfolio, invoker=invoker, fixed_quantity=100)
    
    print("-----------------------------------------------------")

    # --- Test Strategy Engine (Mean Reversion) (Task 5, 6, 7) ---
    print("\n--- Testing Strategy Engine (Mean Reversion) ---")
    mean_rev_strategy = MeanReversionStrategy()
    engine = TradingEngine(mean_rev_strategy)

    # ATTACH ALL observers
    print("Attaching observers...")
    engine.attach(logger)
    engine.attach(alerter)
    engine.attach(order_executor) # <-- Attach the new OrderObserver

    # Create mock data (make sure window in json is small, e.g., 5)
    mock_feed_mr = [
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 30, 0), symbol='AAPL', price=100.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 31, 0), symbol='AAPL', price=101.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 32, 0), symbol='AAPL', price=102.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 33, 0), symbol='AAPL', price=101.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 34, 0), symbol='AAPL', price=100.0), # Window full (5)
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 35, 0), symbol='AAPL', price=80.0),  # Should trigger BUY
        MarketDataPoint(timestamp=datetime(2025, 1, 1, 9, 36, 0), symbol='AAPL', price=120.0)  # Should trigger SELL
    ]

    engine.run(mock_feed_mr)
    
    print("\n--- Testing Strategy Engine (Breakout) ---")
    breakout_strategy = BreakoutStrategy()
    engine2 = TradingEngine(breakout_strategy)
    
    # ATTACH observers
    print("Attaching observers...")
    engine2.attach(logger)
    engine2.attach(alerter)
    engine2.attach(order_executor) # <-- Attach the new OrderObserver

    # Create mock data (make sure window in json is small, e.g., 4)
    mock_feed_bo = [
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 30, 0), symbol='MSFT', price=200.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 31, 0), symbol='MSFT', price=201.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 32, 0), symbol='MSFT', price=200.0),
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 33, 0), symbol='MSFT', price=201.0), # Window full (4)
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 34, 0), symbol='MSFT', price=205.0), # Should trigger BUY
        MarketDataPoint(timestamp=datetime(2025, 1, 2, 9, 35, 0), symbol='MSFT', price=195.0)  # Should trigger SELL
    ]
    
    engine2.run(mock_feed_bo)
    print("---------------------------------")
    
    # --- Test Undo Functionality (Task 7) ---
    print("\n--- Testing Undo/Redo ---")
    print("Undoing last 2 commands...")
    invoker.undo_last_command() # Undoes the MSFT SELL
    invoker.undo_last_command() # Undoes the MSFT BUY
    
    print("\nFinal Portfolio State:")
    print(f"Cash: ${portfolio.cash:,.2f}")
    print(f"Positions: {portfolio.positions}")
    print("-------------------------")