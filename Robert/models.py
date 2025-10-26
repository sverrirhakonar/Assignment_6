from dataclasses import dataclass, field
from datetime import datetime
from datetime import date
import pandas as pd 
from typing import List, Dict

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class Instrument:
    """Base class for financial instruments."""
    def __init__(self, symbol, price, issuer, **kwargs):
        self.symbol = symbol
        self.price = price
        self.issuer = issuer

class Stock(Instrument):
    """Stock instrument."""
    def __init__(self, symbol, price, issuer, sector, **kwargs):
        super().__init__(symbol, price, issuer, **kwargs)
        self.sector = sector

class Bond(Instrument):
    """Bond instrument."""
    def __init__(self, symbol, price, issuer, sector, maturity, **kwargs):
        super().__init__(symbol, price, issuer, **kwargs)
        self.sector = sector
        self.maturity = maturity
        # Convert string to date object during initialization
        try:
            # Attempt to parse YYYY-MM-DD
            self.maturity_date: date | None = pd.to_datetime(maturity).date()
        except (ValueError, TypeError):
             # Handle cases where maturity_str might be empty, None, or unparseable
            self.maturity_date: date | None = None

class ETF(Instrument):
    """ETF instrument."""
    def __init__(self, symbol, price, issuer, sector, **kwargs): # Using sector as per data
        super().__init__(symbol, price, issuer, **kwargs)
        self.sector = sector 

@dataclass
class Position:
    symbol: str
    quantity: float
    price: float

    def value(self) -> float:
        return self.quantity * self.price

@dataclass
class Portfolio:
    name: str
    owner: str | None = None
    positions: List[Position] = field(default_factory=list)
    sub_portfolios: Dict[str, "Portfolio"] = field(default_factory=dict)

    def get_value(self) -> float:
        v = sum(p.value() for p in self.positions)
        v += sum(sp.get_value() for sp in self.sub_portfolios.values())
        return v

    def get_positions(self) -> List[Position]:
        # flatten if you want the composite style API
        out = list(self.positions)
        for sp in self.sub_portfolios.values():
            out.extend(sp.get_positions())
        return out
