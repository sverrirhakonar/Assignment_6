from patterns.Factory import InstrumentFactory
from patterns.Builder import PortfolioBuilder
from data_loader import YahooFinanceAdapter, BloombergXMLAdapter, read_csv_to_immutable_list
from models import Broker, Stock
from patterns.Strategy import BreakoutStrategy, MeanReversionStrategy
from patterns.Observer import SignalPublisher
from reporting import LoggerObserver, AlertObserver
from patterns.Command import ExecuteOrderCommand, CommandInvoker
from analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator
import pandas as pd

# Testing the factory
print("----------------------------------------------------------")
print("Testing the factory.")
print("----------------------------------------------------------")
import csv

with open("Project/data/instruments.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in list(reader):
        instrument = InstrumentFactory.create_instrument(row)
        print(instrument)

print("----------------------------------------------------------")
print("Testing the builder.")
print("----------------------------------------------------------")
portfolio = PortfolioBuilder.from_json("Project/data/portfolio_structure.json")
print(portfolio.name, portfolio.owner)


print("----------------------------------------------------------")
print("Testing the analytics.")
print("----------------------------------------------------------")
# fake price data just for demonstration
asset_prices  = pd.Series([214, 218, 210, 230, 231, 233, 230, 245])
market_prices = pd.Series([100, 100, 101, 101, 102, 103, 104, 104])

wm = Stock(symbol="WM", price=asset_prices.iloc[-1], issuer="Waste Management Inc.", sector="Industrial")

decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(wm, asset_prices, periods_per_year=12), asset_prices, market_prices),asset_prices)

print(decorated.get_metrics())
print("----------------------------------------------------------")
print("Testing the data loader (ingestion from external_data_yahoo.json and external_data_bloomberg.xml)")
print("----------------------------------------------------------")
# Testing the data loader
yahoo = YahooFinanceAdapter("Project/data/external_data_yahoo.json")
bloomberg = BloombergXMLAdapter("Project/data/external_data_bloomberg.xml")

meta = yahoo.get_data("META")
msft = bloomberg.get_data("MSFT")

print(meta)
print(msft)
print("----------------------------------------------------------")
print("Testing the composite pattern (recursive aggregation from portfolio_structure.json.)")
print("----------------------------------------------------------")
# Composite pattern: Demonstrate recursive aggregation from portfolio_structure.json.
print("The main portfolio value:", portfolio.get_value())
for position in portfolio.positions:
    print(f"  {position.symbol} value:", position.get_value())
for sub_name, sub in portfolio.sub_portfolios.items():
    print(f"  {sub_name} value:", sub.get_value())
    for position in sub.positions:
        print(f"    {position.symbol} value:", position.get_value())


print("----------------------------------------------------------")
print("Testing the strategy interchangeability and signal generation.")
print("----------------------------------------------------------")
ticks = read_csv_to_immutable_list("Project/data/market_data.csv")
strategies = [BreakoutStrategy(), MeanReversionStrategy()]

for strat in strategies:
    print(f"\nUsing strategy: {strat.__class__.__name__}")
    signals = []
    for tick in ticks:
        new_signals = strat.generate_signals(tick)
        signals.extend(new_signals)

    if signals:
        for s in signals[:5]: 
            print(f"Generated signal: {s}")
    else:
        print("No signals generated (strategy thresholds not triggered).")

print("----------------------------------------------------------")
print("Testing the dynamic observer registration and notification.")
print("----------------------------------------------------------")
pub = SignalPublisher()

logger = LoggerObserver()
alert = AlertObserver(min_notional=500)

print("Attaching observers...")
pub.attach(logger)
pub.attach(alert)

# Send small and large signals
pub.notify({"timestamp": "t5", "symbol": "AAPL", "action": "BUY", "price": 50, "qty": 5})
pub.notify({"timestamp": "t6", "symbol": "AAPL", "action": "BUY", "price": 200, "qty": 5})

print("Detaching alert observer...")
pub.detach(alert)
pub.notify({"timestamp": "t7", "symbol": "AAPL", "action": "SELL", "price": 150, "qty": 1})


print("----------------------------------------------------------")
print("Testing the trade lifecycle: signal → execution → undo → redo.")
print("----------------------------------------------------------")

broker = Broker(starting_cash=10000)
invoker = CommandInvoker()

order = {
    "timestamp": "t8",
    "symbol": "AAPL",
    "side": "BUY",
    "qty": 10,
    "price": 100,
}

cmd = ExecuteOrderCommand(broker, order)

print("Executing order...")
invoker.do(cmd)
print("After execution:", broker.summary())

print("Undoing last trade...")
invoker.undo()
print("After undo:", broker.summary())

print("Redoing last trade...")
invoker.redo()
print("After redo:", broker.summary())

print("----------------------------------------------------------")
print("Thank you for runnign the program!")


