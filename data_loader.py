# In data_loader.py
import json
from datetime import datetime
from models import MarketDataPoint # Import your standard object
import xml.etree.ElementTree as ET # Import Python's built-in XML parser

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

class BloombergXMLAdapter:
    """Adapts Bloomberg XML data format to MarketDataPoint objects."""
    def __init__(self, filepath: str):
        self.filepath = filepath
        # Store data indexed by symbol after parsing
        self._data_by_symbol: dict[str, ET.Element] = self._load_and_parse_data()

    def _load_and_parse_data(self) -> dict[str, ET.Element]:
        """Loads and parses the XML file, indexing instrument elements by symbol."""
        indexed_data = {}
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()

            for instrument_element in root.findall('instrument'):
                symbol_element = instrument_element.find('symbol') # Find the <symbol> tag
                if symbol_element is not None and symbol_element.text:
                    symbol = symbol_element.text.strip() # Get text content of <symbol>
                    indexed_data[symbol] = instrument_element # Store the <instrument> element
                else:
                    print(f"Warning: Skipping instrument element with missing/empty symbol tag in {self.filepath}")

            print(f" -> Successfully loaded and parsed: {self.filepath}")
            return indexed_data

        except FileNotFoundError:
            print(f"Error: Bloomberg XML file not found at {self.filepath}")
            return {}
        except ET.ParseError:
            print(f"Error: Could not parse XML from {self.filepath}")
            return {}
        except Exception as e:
            print(f"Error loading {self.filepath}: {e}")
            return {}

    def get_data(self, symbol: str):
        """Retrieves data for a symbol and adapts it to MarketDataPoint."""
        instrument_element = self._data_by_symbol.get(symbol) # Efficient lookup
        if instrument_element is None:
            print(f"Warning: Symbol '{symbol}' not found in Bloomberg XML data.")
            return None
        try:
            price_element = instrument_element.find('price')         # Use 'price' tag
            timestamp_element = instrument_element.find('timestamp') # Use 'timestamp' tag

            if price_element is None or price_element.text is None:
                raise ValueError("Missing or empty 'price' tag")
            if timestamp_element is None or timestamp_element.text is None:
                raise ValueError("Missing or empty 'timestamp' tag")

            price = float(price_element.text)
            timestamp_str = timestamp_element.text

            timestamp_dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return MarketDataPoint(timestamp=timestamp_dt, symbol=symbol, price=price)

        except (ValueError, TypeError) as e: # Catches float conversion or None.text errors
            print(f"Warning: Error converting/finding data for symbol '{symbol}' in Bloomberg XML: {e}")
            return None
        
        except Exception as e: # Catch other potential errors like invalid timestamp
            print(f"Warning: Unexpected error processing symbol '{symbol}' in Bloomberg XML: {e}")
            return None