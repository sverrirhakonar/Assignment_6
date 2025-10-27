from typing import Dict, Any, Type
from models import Instrument, Stock, Bond, ETF

class InstrumentFactory:
    # Maps type names to classes
    _registry: Dict[str, Type[Instrument]] = {
        "stock": Stock,
        "bond": Bond,
        "etf": ETF,
    }

    @classmethod
    def register(cls, kind: str, instrument_class: Type[Instrument]) -> None:
        """
        Add a new instrument type to the registry.
        Example: InstrumentFactory.register("future", Future)
        """
        cls._registry[kind.lower()] = instrument_class

    @classmethod
    def create_instrument(cls, data: Dict[str, Any]) -> Instrument:
        """
        Create an instrument using CSV-like data.

        Expected keys (based on your CSV):
          - type (e.g., "Stock", "Bond", "ETF")  [required]
          - symbol                                [required]
          - issuer                                [required; replaces 'name']
          - price                                 [optional but expected in your CSV]
          - sector                                [optional but expected in your CSV]
          - maturity                              [optional; treated as extra field]

        Any fields not in {type, symbol, issuer, price, sector} will be passed
        through via **extra_fields (e.g., 'maturity').
        """
        # 1) Validate and normalize type
        if "type" not in data:
            raise ValueError("Each instrument must have a 'type' field (e.g., stock, bond, etf).")
        kind = str(data["type"]).lower()
        if kind not in cls._registry:
            raise ValueError(f"Unknown instrument type: {kind}")
        instrument_class = cls._registry[kind]

        # 2) Required shared fields
        symbol = data.get("symbol")
        if not symbol:
            raise ValueError("Each instrument must have a 'symbol' field.")
        issuer = data.get("issuer")
        if not issuer:
            raise ValueError("Each instrument must have an 'issuer' field (used instead of 'name').")

        # 3) Common optional fields
        price = data.get("price")
        sector = data.get("sector")

        # 4) Extra fields 
        extra_fields = {
            key: value
            for key, value in data.items()
            if key not in {"type", "symbol", "issuer", "price", "sector"}
        }

        # 5) Build and return the instrument
        return instrument_class(
            symbol=symbol,
            issuer=issuer,
            price=price,
            sector=sector,
            **extra_fields
        )
