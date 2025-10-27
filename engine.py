# In engine.py
from models import MarketDataPoint
from patterns.strategy import Strategy
from patterns.observer import SignalPublisher, Observer # <-- Import publisher and observer
from typing import List

class TradingEngine:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        # Create an instance of SignalPublisher to manage observers
        self.publisher = SignalPublisher()
        print(f"TradingEngine initialized with strategy: {strategy.__class__.__name__}")

    def attach(self, observer: Observer):
        self.publisher.attach(observer)

    def run(self, data_feed: List[MarketDataPoint]):
        print(f"--- Running engine over {len(data_feed)} data points ---")
        for tick in data_feed:
            # Get the list of signals (e.g., ['BUY'] or []) from the strategy
            signals = self.strategy.generate_signals(tick)

            if signals:
                # Loop through any signals generated (usually just one)
                for signal_action in signals:
                    # Create the signal dictionary (the event data)
                    signal_event = {
                        'timestamp': tick.timestamp,
                        'signal': signal_action, # 'BUY' or 'SELL'
                        'symbol': tick.symbol,
                        'price': tick.price,
                        'strategy': self.strategy.__class__.__name__
                    }

                    print(f"  -> Publishing Signal: {signal_action} {tick.symbol}") # For debugging
                    self.publisher.notify(signal_event)

            # If the list is empty (HOLD), we do nothing.
        print("--- Engine run complete ---")