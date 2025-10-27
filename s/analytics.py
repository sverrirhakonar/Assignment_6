# In analytics.py
from abc import ABC, abstractmethod
from models import Instrument # Import the base class we're decorating
import numpy as np # We'll need numpy for calculations
# We'll need a way to get historical data,
# but for now, we'll just mock it inside the decorator.
import pandas as pd
# d
# --- 1. Abstract Decorator ---
class InstrumentDecorator(Instrument, ABC):
    _wrapped_instrument: Instrument = None

    def __init__(self, instrument: Instrument):
        # Note: We don't call super().__init__() because Instrument's
        # __init__ would set attributes. We just wrap.
        self._wrapped_instrument = instrument

    def get_metrics(self) -> dict:
        # Get the metrics dictionary from the object we're wrapping
        return self._wrapped_instrument.get_metrics()

    # --- We must also "pass through" other base class properties ---
    # This ensures the decorator still "looks like" an Instrument.
    @property
    def symbol(self):
        return self._wrapped_instrument.symbol

    @property
    def price(self):
        return self._wrapped_instrument.price
    
    @property
    def issuer(self):
        return self._wrapped_instrument.issuer


class VolatilityDecorator(InstrumentDecorator):
    """
    Concrete decorator that adds a volatility calculation.
    """
    def __init__(self, instrument: Instrument, history_days: int = 20):
        # Call the parent decorator's __init__ to store the instrument
        super().__init__(instrument)
        self.history_days = history_days # Store specific param for this analytic

    def _get_mock_historical_data(self) -> np.ndarray:
        """
        Mock function to simulate fetching historical data.
        In a real system, this would query a database or API.
        """
        print(f"  ... (Mock Fetch): Fetching {self.history_days} days of prices for {self.symbol} ...")
        # Generate some fake log-normal price data
        np.random.seed(42) # for reproducible results
        log_returns = np.random.normal(0.0001, 0.02, self.history_days)
        # Start from the current price and work backwards (simplified)
        price_changes = np.exp(log_returns)
        # This isn't a perfect simulation, just gives us numbers to work with
        mock_prices = self.price * np.cumprod(price_changes) 
        return mock_prices

    def get_metrics(self) -> dict:
        """
        Overrides the base method to add volatility.
        """
        # 1. First, get the metrics dictionary from the object we're wrapping
        #    (This calls super().get_metrics(), which calls self._wrapped_instrument.get_metrics())
        metrics = super().get_metrics()
        
        # 2. Now, add our new analytic
        try:
            # Get (mock) historical data
            historical_prices = self._get_mock_historical_data()
            
            # Calculate (mock) log returns
            log_returns = np.log(historical_prices[1:] / historical_prices[:-1])
            
            # Calculate annualized volatility
            # (Daily std dev * sqrt(252 trading days))
            annualized_vol = np.std(log_returns) * np.sqrt(252)
            
            metrics['annualized_volatility'] = round(annualized_vol, 4)
        
        except Exception as e:
            metrics['annualized_volatility'] = f"Error: {e}"
            
        # 3. Return the *modified* metrics dictionary
        return metrics