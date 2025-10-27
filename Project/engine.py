# engine.py
from models import Broker, MarketDataPoint
from patterns.Strategy import Strategy
from patterns.Command import ExecuteOrderCommand, CommandInvoker

class Engine:
    def __init__(self, strategy: Strategy, broker: Broker, publisher=None):
        self.strategy = strategy
        self.broker = broker
        self.publisher = publisher
        self.invoker = CommandInvoker()

    def on_tick(self, tick: MarketDataPoint):
        # Update latest price
        self.broker.update_price(tick)

        # Get signals from the strategy
        signals = self.strategy.generate_signals(tick)

        for sig in signals:
            # Notify any observers (logger, alert)
            if self.publisher:
                self.publisher.notify(sig)

            # Convert signal -> command
            order = {
                "timestamp": sig["timestamp"],
                "symbol": sig["symbol"],
                "side": "BUY" if sig["action"] == "BUY" else "SELL",
                "qty": sig.get("qty", 1),
                "price": float(sig["price"]),
            }

            cmd = ExecuteOrderCommand(self.broker, order)
            self.invoker.do(cmd)

    def run(self, ticks):
        for tick in ticks:
            self.on_tick(tick)

    def undo_last(self):
        self.invoker.undo()

    def redo_last(self):
        self.invoker.redo()

    def summary(self):
        print("Engine summary:", self.broker.summary())
