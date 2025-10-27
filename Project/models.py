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


class Broker:
    """Handles cash, positions, and trade execution."""

    def __init__(self, starting_cash: float = 0.0):
        self.cash = float(starting_cash)
        self.last_price: Dict[str, float] = {}
        self.root_portfolio = Portfolio(name="MainPortfolio")
        self.trades = []

    def update_price(self, tick: MarketDataPoint):
        self.last_price[tick.symbol] = tick.price

    def execute_order(self, symbol: str, side: str, qty: float, price: float):
        """Executes a simple market order and updates the portfolio."""
        if side == "BUY":
            self.cash -= price * qty
            self._adjust_position(symbol, qty, price)
        elif side == "SELL":
            self.cash += price * qty
            self._adjust_position(symbol, -qty, price)

        self.trades.append({"symbol": symbol, "side": side, "qty": qty, "price": price})

    def _adjust_position(self, symbol: str, delta_qty: float, price: float):
        """Update or create a position in the root portfolio."""
        pos = next((p for p in self.root_portfolio.positions if p.symbol == symbol), None)
        if pos:
            pos.quantity += delta_qty
            pos.price = price
            if abs(pos.quantity) < 1e-9:  # flat
                self.root_portfolio.positions.remove(pos)
        else:
            if delta_qty > 0:
                self.root_portfolio.add_position(Position(symbol, delta_qty, price))

    def equity(self):
        # Total = cash + portfolio value using last prices
        port_value = 0
        for pos in self.root_portfolio.positions:
            price = self.last_price.get(pos.symbol, pos.price)
            port_value += pos.quantity * price
        return self.cash + port_value

    def summary(self):
        return {
            "cash": round(self.cash, 2),
            "equity": round(self.equity(), 2),
            "positions": [
                {"symbol": p.symbol, "qty": p.quantity, "price": p.price}
                for p in self.root_portfolio.positions
            ],
            "n_trades": len(self.trades),
        }