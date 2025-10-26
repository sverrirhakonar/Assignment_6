# In patterns/factory.py
from models import Stock, Bond, ETF # Import the classes to be created

class InstrumentFactory:

    @staticmethod # Use staticmethod as creation doesn't depend on factory instance state
    def create_instrument(data: dict):
        try:
            instrument_type = data.get('type') # Use .get() for safer access
            if not instrument_type:
                print(f"Warning: Missing 'type' in data row: {data}. Skipping.")
                return None

            symbol = data['symbol']
            price = float(data['price']) 
            issuer = data['issuer']
            sector = data['sector']

            if instrument_type == 'Stock':
                return Stock(symbol=symbol, price=price, issuer=issuer, sector=sector)
            elif instrument_type == 'Bond':
                maturity = data['maturity']
                return Bond(symbol=symbol, price=price, issuer=issuer, sector=sector, maturity_str=maturity)
            elif instrument_type == 'ETF':
                return ETF(symbol=symbol, price=price, issuer=issuer, sector=sector)
            else:
                print(f"Warning: Unknown instrument type '{instrument_type}' for symbol '{symbol}'. Skipping.")
                return None

        except KeyError as e:
            # Handle missing required keys for the specific type
            print(f"Warning: Missing expected key {e} for type '{instrument_type}' in data: {data}. Skipping.")
            return None
        except ValueError as e:
            # Handle error during float conversion
            print(f"Warning: Error converting price for data: {data} ({e}). Skipping.")
            return None
        except Exception as e:
            # Catch-all for other unexpected errors during creation
            print(f"Warning: Unexpected error creating instrument for data: {data} ({e}). Skipping.")
            return None