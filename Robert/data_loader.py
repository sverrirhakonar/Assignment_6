import json
import xml.etree.ElementTree as ET
from datetime import datetime
from models import MarketDataPoint

# This parse iso is for the timestamp in Yahoo data.
def _parse_iso(ts: str) -> datetime:
    """Convert ISO string like '2025-10-01T09:30:00Z' to datetime."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


class YahooFinanceAdapter:
    """
    Reads Yahoo Finance JSON data format to MarketDataPoint objects.
    """
    def __init__(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def get_data(self, symbol: str) -> MarketDataPoint | None:
        if not isinstance(self._data, dict):
            return None
        if str(self._data.get("ticker")) != symbol:
            return None
        return MarketDataPoint(
            timestamp=_parse_iso(self._data["timestamp"]),
            symbol=self._data["ticker"],
            price=float(self._data["last_price"]),
        )

class BloombergXMLAdapter:
    """
    Reads Bloomberg XML data format to MarketDataPoint objects.
    """
    def __init__(self, path: str):
        self._root = ET.parse(path).getroot()

    def get_data(self, symbol: str):
        # Directly extract from the root <instrument>
        sym = self._root.findtext("symbol")
        if sym != symbol:
            return None
        price = float(self._root.findtext("price"))
        ts = _parse_iso(self._root.findtext("timestamp"))
        return MarketDataPoint(timestamp=ts, symbol=sym, price=price)


