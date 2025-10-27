# In patterns/strategy.py
from abc import ABC, abstractmethod
from collections import deque
import numpy as np # We'll need numpy for mean and std dev
from models import MarketDataPoint # Assuming this is where MarketDataPoint is
from patterns.singleton import Config # To get strategy parameters

class Strategy(ABC):

    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

class MeanReversionStrategy(Strategy):
    """A strategy that generates signals based on mean reversion."""
    def __init__(self):
        config = Config() 
        params = config.get_setting('strategy_params.MeanReversionStrategy', {})
        self.lookback_window = params.get('lookback_window', 20)
        self.threshold = params.get('threshold', 2.0) # e.g., 2.0 standard deviations
        self.prices = deque(maxlen=self.lookback_window)

    def generate_signals(self, tick: MarketDataPoint) -> int:
        """Generates 1 (BUY), -1 (SELL), or 0 (HOLD) signal."""
        self.prices.append(tick.price)
        signal = [] # Default signal is 0 (HOLD)

        if len(self.prices) < self.lookback_window:
            return signal # Not enough data

        np_prices = np.array(self.prices)
        current_mean = np.mean(np_prices)
        current_std = np.std(np_prices)

        if current_std == 0:
            return signal # Avoid division by zero, no signal
        
        z_score = (tick.price - current_mean) / current_std
        
        if z_score < -self.threshold:
            signal = ['BUY'] # Price is low, signal BUY
        elif z_score > self.threshold:
            signal = ['SELL'] # Price is high, signal SELL
        
        return signal

class BreakoutStrategy(Strategy):
    """A strategy that signals BUY on new highs and SELL on new lows."""
    def __init__(self):
        super().__init__() # Call base __init__
        config = Config()

        params = config.get_setting('strategy_params.BreakoutStrategy', {})
        self.lookback_window = params.get('lookback_window', 15)
        self.prices = deque(maxlen=self.lookback_window)

    def generate_signals(self, tick: MarketDataPoint) -> int:
        """Generates 1 (BUY), -1 (SELL), or 0 (HOLD) signal."""
        signal = []
        
        previous_prices = list(self.prices)
        self.prices.append(tick.price) 

        if len(self.prices) < self.lookback_window:
            return signal 

        if not previous_prices: 
             return signal
             
        recent_high = max(previous_prices)
        recent_low = min(previous_prices)
        
        if tick.price > recent_high:
            signal = ['BUY'] # Price broke above recent high, BUY
        elif tick.price < recent_low:
            signal = ['SELL'] # Price broke below recent low, SELL
        
        return signal