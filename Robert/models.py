from dataclasses import dataclass, field
from datetime import datetime, date
#from datetime import date
import pandas as pd 
from typing import List, Dict
from abc import ABC, abstractmethod


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


class PortfolioComponent(ABC):
    """Makes sure that the Portfolio and Position classes have the get_value and get_positions methods."""

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_positions(self):
        pass

@dataclass
class Position(PortfolioComponent):
    symbol = None
    quantity = 0
    price = 0

    def __init__(self, symbol, quantity, price):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

    def value(self):
        """Helper method — not part of the interface, just a convenience."""
        return self.quantity * self.price

    def get_value(self):
        return self.value()

    def get_positions(self):
        return [self]

@dataclass
class Portfolio(PortfolioComponent):
    name: str
    owner: str = None
    positions: list = field(default_factory=list)
    sub_portfolios: dict = field(default_factory=dict)

    def add_position(self, position):
        self.positions.append(position)

    def add_subportfolio(self, sub):
        self.sub_portfolios[sub.name] = sub

    def get_value(self):
        total = sum(p.get_value() for p in self.positions)
        total += sum(sp.get_value() for sp in self.sub_portfolios.values())
        return total

    def get_positions(self):
        out = list(self.positions)
        for sp in self.sub_portfolios.values():
            out.extend(sp.get_positions())
        return out
