# In reporting.py
from patterns.observer import Observer
import logging # We can use the logging module for the logger
import datetime # To add timestamps to logs

# --- Optional: Set up a simple logger (writes to a file) ---
# This setup is basic; a real app might configure this in main.py
try:
    logging.basicConfig(
        filename='trade_signals.log', # Log to this file
        level=logging.INFO, # Log INFO level and above
        format='%(asctime)s - %(message)s', # Log format
        datefmt='%Y-%m-%d %H:%M:%S'
    )
except PermissionError:
    print("Warning: No permission to write to 'trade_signals.log'. LoggerObserver will only print to console.")
# --- End optional setup ---


class LoggerObserver(Observer):
    """
    An observer that logs every signal to a file and/or the console.
    """
    def update(self, signal: dict):
        """
        Receives signal update and logs it.
        """
        log_message = (
            f"SIGNAL LOG: "
            f"Time={signal.get('timestamp')}, "
            f"Strategy={signal.get('strategy')}, "
            f"Symbol={signal.get('symbol')}, "
            f"Signal={signal.get('signal')}, "
            f"Price={signal.get('price')}"
        )
        
        # Log to the configured file (if setup was successful)
        logging.info(log_message)
        
        # Also print to console for immediate visibility
        print(log_message)

class AlertObserver(Observer):
    """
    An observer that prints a high-visibility alert for any signal.
    """
    def update(self, signal: dict):
        """
        Receives signal update and prints a loud alert.
        """
        # In a real system, this might send an email, a text message,
        # or alert only if the trade value is very large.
        # For now, it just prints a formatted alert for *every* signal.
        
        print("\n" + "*"*30)
        print(f"!!! ALERT !!!")
        print(f"  Timestamp: {signal.get('timestamp')}")
        print(f"  Strategy:  {signal.get('strategy')}")
        print(f"  Action:    {signal.get('signal')}")
        print(f"  Symbol:    {signal.get('symbol')}")
        print(f"  Price:     {signal.get('price')}")
        print("*"*30 + "\n")