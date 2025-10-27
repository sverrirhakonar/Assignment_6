import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from patterns.Observer import SignalPublisher


class TestObserver:
    """Simple observer that records every signal it receives."""
    def __init__(self, name):
        self.name = name
        self.signals = []

    def update(self, signal: dict):
        # Store a copy to ensure the original dict can mutate without affecting our record
        self.signals.append(dict(signal))


def test_observer_attach_detach_notify():
    pub = SignalPublisher()
    a = TestObserver("A")
    b = TestObserver("B")

    # Attach both observers
    pub.attach(a)
    pub.attach(b)

    # Notify once
    sig1 = {"timestamp": "t1", "symbol": "ADSK", "action": "BUY", "price": 100.0, "qty": 5}
    pub.notify(sig1)

    assert len(a.signals) == 1
    assert len(b.signals) == 1
    assert a.signals[0]["symbol"] == "ADSK"
    assert b.signals[0]["action"] == "BUY"

    # Detach one observer and notify again
    pub.detach(b)
    sig2 = {"timestamp": "t2", "symbol": "ADSK", "action": "SELL", "price": 101.0, "qty": 3}
    pub.notify(sig2)

    # A should have 2 notifications, B should still have 1
    assert len(a.signals) == 2
    assert len(b.signals) == 1
    assert a.signals[-1]["action"] == "SELL"