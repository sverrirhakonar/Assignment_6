# In engine.py
from models import MarketDataPoint
from patterns.strategy import Strategy # Import the base class for type hinting
from typing import List

class TradingEngine:

    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        print(f"TradingEngine initialized with strategy: {strategy.__class__.__name__}")

    def run(self, data_feed: List[MarketDataPoint]):
        print(f"--- Running engine over {len(data_feed)} data points ---")
        for tick in data_feed:
            # Get the list of signals (e.g., ['BUY'] or []) from the strategy
            signals = self.strategy.generate_signals(tick)
            if signals:

                for signal_action in signals:
                    if signal_action == 'BUY':
                        # Later, this will publish a BUY signal (Task 6)
                        print(f"  -> {tick.timestamp}: BUY {tick.symbol} at {tick.price}")
                    elif signal_action == 'SELL':
                        # Later, this will publish a SELL signal (Task 6)
                        print(f"  -> {tick.timestamp}: SELL {tick.symbol} at {tick.price}")
                    # If signal is 'HOLD' or anything else, we can ignore it
            
