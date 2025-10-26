# In data_loader.py
import json
from datetime import datetime
from models import MarketDataPoint # Import your standard object


class YahooFinanceAdapter:
    """Adapts Yahoo Finance JSON data format to MarketDataPoint objects."""
    def __init__(self, filepath: str):
        self.filepath = filepath
        # Store data indexed by symbol for faster lookup
        self._data_by_symbol: dict[str, dict[str, any]] = self._load_and_index_data()

    def _load_and_index_data(self) -> dict[str, dict[str, any]]:
        """Loads JSON data (assumed list of dicts) and indexes it by ticker."""
        indexed_data = {}
        try:
            with open(self.filepath, 'r') as f:
                data_list = json.load(f)
                if not isinstance(data_list, list):
                    if isinstance(data_list, dict) and 'ticker' in data_list:
                         data_list = [data_list] # Treat single object as list of one
                    else:
                         print(f"Error: Expected list in {self.filepath}, found {type(data_list)}")
                         return {}
                for item in data_list:
                    if isinstance(item, dict) and 'ticker' in item:
                        indexed_data[item['ticker']] = item
                    else:
                         print(f"Warning: Skipping invalid item in {self.filepath}: {item}")
            print(f" -> Successfully loaded and indexed: {self.filepath}")
            return indexed_data
        except FileNotFoundError:
            print(f"Error: Yahoo data file not found at {self.filepath}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.filepath}")
            return {}
        except Exception as e:
            print(f"Error loading {self.filepath}: {e}")
            return {}

    def get_data(self, symbol: str) -> MarketDataPoint | None:
        """Retrieves data for a symbol and adapts it to MarketDataPoint."""
        symbol_data = self._data_by_symbol.get(symbol)
        if not symbol_data:
            print(f"Warning: Symbol '{symbol}' not found in Yahoo data.")
            return None
        try:
            timestamp_str = symbol_data['timestamp']
            price = float(symbol_data['last_price'])
            timestamp_dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return MarketDataPoint(timestamp=timestamp_dt, symbol=symbol_data['ticker'], price=price)
        except (KeyError, ValueError, Exception) as e:
            print(f"Warning: Error processing symbol '{symbol}' in Yahoo data: {e}")
            return None

# --- We will add BloombergXMLAdapter class here later ---