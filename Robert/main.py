from patterns.Factory import InstrumentFactory
from patterns.Builder import PortfolioBuilder

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
