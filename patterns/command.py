
# In patterns/command.py
from abc import ABC, abstractmethod
from portfolio import Portfolio # Import the receiver

# --- 1. Command Interface ---
class Command(ABC):
    """Abstract base class for all commands."""
    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self):
        """Undo the command."""
        pass

class BuyOrderCommand(Command):
    """
    A command to execute a BUY order.
    It holds all info needed to execute and undo the trade.
    """
    def __init__(self, portfolio: Portfolio, symbol: str, price: float, quantity: int = 100):
        self.portfolio = portfolio # The 'Receiver'
        self.symbol = symbol
        self.price = price
        self.quantity = quantity # Assuming fixed quantity

    def execute(self):
        """Executes the trade (calls the receiver's buy method)."""
        print(f"COMMAND: Executing BUY {self.quantity} {self.symbol}...")
        self.portfolio.buy(self.symbol, self.quantity, self.price)

    def undo(self):
        """Undoes the trade (calls the receiver's sell method)."""
        print(f"COMMAND: Undoing BUY {self.quantity} {self.symbol}...")
        self.portfolio.sell(self.symbol, self.quantity, self.price)

class SellOrderCommand(Command):
    """
    A command to execute a SELL order.
    It holds all info needed to execute and undo the trade.
    """
    def __init__(self, portfolio: Portfolio, symbol: str, price: float, quantity: int = 100):
        self.portfolio = portfolio # The 'Receiver'
        self.symbol = symbol
        self.price = price
        self.quantity = quantity # Assuming fixed quantity

    def execute(self):
        """Executes the trade (calls the receiver's sell method)."""
        print(f"COMMAND: Executing SELL {self.quantity} {self.symbol}...")
        self.portfolio.sell(self.symbol, self.quantity, self.price)

    def undo(self):
        """Undoes the trade (calls the receiver's buy method)."""
        print(f"COMMAND: Undoing SELL {self.quantity} {self.symbol}...")
        self.portfolio.buy(self.symbol, self.quantity, self.price)

class CommandInvoker:
    """
    The 'Invoker' class. It takes commands, executes them,
    and keeps a history to support undo.
    """
    def __init__(self):
        self._history: list[Command] = [] # A list to act as a command history

    def execute_command(self, command: Command):
        """
        Executes a given command and adds it to the history.
        """
        try:
            command.execute()
            self._history.append(command)
        except Exception as e:
            print(f"INVOKER: Error executing command {command.__class__.__name__}: {e}")

    def undo_last_command(self):
        """
        Undoes the most recent command from the history.
        """
        if not self._history:
            print("INVOKER: No commands to undo.")
            return

        try:
            # Pop the last command from the history
            last_command = self._history.pop()
            # Call its undo method
            last_command.undo()
        except Exception as e:
            print(f"INVOKER: Error undoing command {last_command.__class__.__name__}: {e}")