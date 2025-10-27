from dataclasses import dataclass
from datetime import datetime
from datetime import date
import pandas as pd # Assuming pandas is used later for date conversion

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class Instrument:
    """Base class for financial instruments."""
    def __init__(self, symbol, price, issuer):
        self.symbol = symbol
        self.price = price
        self.issuer = issuer

    def get_metrics(self) -> dict:
        return {
            'symbol': self.symbol,
            'price': self.price
        }

class Stock(Instrument):
    """Represents a stock instrument."""
    def __init__(self, symbol, price, issuer, sector):
        super().__init__(symbol, price, issuer)
        self.sector = sector

class Bond(Instrument):
    """Represents a bond instrument."""
    def __init__(self, symbol, price, issuer, sector, maturity_str):
        super().__init__(symbol, price, issuer)
        self.sector = sector
        self.maturity_str = maturity_str
        # Optional: convert string to date object during initialization
        try:
            # Attempt to parse YYYY-MM-DD
            self.maturity_date: date | None = pd.to_datetime(maturity_str).date()
        except (ValueError, TypeError):
             # Handle cases where maturity_str might be empty, None, or unparseable
            self.maturity_date: date | None = None

class ETF(Instrument):
    """Represents an ETF instrument."""
    def __init__(self, symbol, price, issuer, sector): # Using sector as per data
        super().__init__(symbol, price, issuer)
        self.sector = sector # e.g., 'Index'


