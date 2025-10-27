import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


class LoggerObserver:
    """Logs all signals."""

    def update(self, signal: dict):
        msg = (
            f"[LOG] {signal['timestamp']} | {signal['symbol']} | "
            f"{signal['action']} @ {signal['price']}"
        )
        logging.info(msg)


class AlertObserver:
    """Alerts on large trades."""

    def __init__(self, min_notional=10000):
        self.min_notional = min_notional

    def update(self, signal: dict):
        qty = signal.get("qty", 1)
        notional = qty * float(signal["price"])
        if notional >= self.min_notional:
            print(f"[ALERT] Large trade detected: {signal['symbol']} {signal['action']} "
                  f"Qty={qty} Notional={notional:.2f}")
