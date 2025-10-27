# In portfolio.py
class Portfolio:
    """
    A simple mock portfolio (the 'Receiver').
    It just prints buy/sell actions and tracks cash.
    """
    def __init__(self, initial_cash: float = 100_000.0):
        self.cash = initial_cash
        self.positions = {} # { 'AAPL': 10, 'MSFT': 5 }
        print(f"Portfolio initialized with ${self.cash:,.2f} cash.")

    def buy(self, symbol: str, quantity: int, price: float):
        """Simulates buying a stock."""
        cost = price * quantity
        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
            print(f"  PORTFOLIO: BOUGHT {quantity} {symbol} @ ${price:,.2f}. Cost: ${cost:,.2f}. Cash left: ${self.cash:,.2f}")
        else:
            print(f"  PORTFOLIO: NOT ENOUGH CASH to buy {quantity} {symbol}. Need ${cost:,.2f}, have ${self.cash:,.2f}")

    def sell(self, symbol: str, quantity: int, price: float):
        """Simulates selling a stock."""
        current_quantity = self.positions.get(symbol, 0)
        if current_quantity >= quantity:
            proceeds = price * quantity
            self.cash += proceeds
            self.positions[symbol] = current_quantity - quantity
            if self.positions[symbol] == 0:
                del self.positions[symbol]
            print(f"  PORTFOLIO: SOLD {quantity} {symbol} @ ${price:,.2f}. Proceeds: ${proceeds:,.2f}. Cash left: ${self.cash:,.2f}")
        else:
            print(f"  PORTFOLIO: NOT ENOUGH SHARES to sell {quantity} {symbol}. Have {current_quantity}.")