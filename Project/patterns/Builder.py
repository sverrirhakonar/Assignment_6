from models import Portfolio, Position
import json


class PortfolioBuilder:
    def __init__(self, name=None):
        self._name = name
        self._owner = None
        self._positions = []
        self._sub_builders = {}

    def set_owner(self, name):
        self._owner = name
        return self

    def add_position(self, symbol, quantity, price):
        self._positions.append(Position(symbol=symbol, quantity=quantity, price=price))
        return self

    def add_subportfolio(self, name, builder):
        self._sub_builders[name] = builder
        return self

    def build(self):
        if not self._name:
            raise ValueError("Portfolio name must be set before build().")

        subs = {name: b.build() for name, b in self._sub_builders.items()}

        return Portfolio(
            name=self._name,
            owner=self._owner,
            positions=list(self._positions),
            sub_portfolios=subs,
        )

    @staticmethod
    def from_dict(data):
        if "name" not in data:
            raise ValueError("Portfolio dict must include 'name'.")

        builder = PortfolioBuilder(data["name"])

        if "owner" in data:
            builder.set_owner(data["owner"])

        for pos in data.get("positions", []):
            builder.add_position(pos["symbol"], pos["quantity"], pos["price"])

        for sub in data.get("sub_portfolios", []):
            sub_builder = PortfolioBuilder.from_dict(sub)
            builder.add_subportfolio(sub["name"], sub_builder)

        return builder

    @staticmethod
    def from_json(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PortfolioBuilder.from_dict(data).build()
