from patterns.Factory import InstrumentFactory
from patterns.Builder import PortfolioBuilder
from data_loader import YahooFinanceAdapter, BloombergXMLAdapter

# Testing the factory
import csv

with open("Robert/data/instruments.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in list(reader):
        instrument = InstrumentFactory.create_instrument(row)
        print(instrument)

# Testing the builder
portfolio = PortfolioBuilder.from_json("Robert/data/portfolio_structure.json")
print(portfolio.name, portfolio.owner)


# main.py (just a few lines somewhere to show it works)
import pandas as pd
from models import Stock  # or your concrete instrument class
from analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator

# fake price data just for demonstration
asset_prices  = pd.Series([214, 218, 210, 230, 231, 233, 230, 245])
market_prices = pd.Series([100, 100, 101, 101, 102, 103, 104, 104])

wm = Stock(symbol="WM", price=asset_prices.iloc[-1], issuer="Waste Management Inc.", sector="Industrial")

decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(wm, asset_prices, periods_per_year=12), asset_prices, market_prices),asset_prices)

print(decorated.get_metrics())

# Testing the data loader
yahoo = YahooFinanceAdapter("Robert/data/external_data_yahoo.json")
bloomberg = BloombergXMLAdapter("Robert/data/external_data_bloomberg.xml")

meta = yahoo.get_data("META")
msft = bloomberg.get_data("MSFT")

print(meta)
print(msft)

# Composite pattern: Demonstrate recursive aggregation from portfolio_structure.json.
print("The main portfolio value:", portfolio.get_value())
for position in portfolio.positions:
    print(f"  {position.symbol} value:", position.get_value())
for sub_name, sub in portfolio.sub_portfolios.items():
    print(f"  {sub_name} value:", sub.get_value())
    for position in sub.positions:
        print(f"    {position.symbol} value:", position.get_value())



