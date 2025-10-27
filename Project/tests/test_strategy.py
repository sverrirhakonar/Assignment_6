import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import MarketDataPoint
from patterns.Strategy import BreakoutStrategy, MeanReversionStrategy

def test_breakout_strategy_signals_expected_behavior():
    """Confirm BreakoutStrategy generates a BUY when price jumps beyond threshold."""

    strat = BreakoutStrategy(lookback_window=3, threshold=0.02)

    # Fake price data where one jump should trigger a breakout BUY
    ticks = [
        MarketDataPoint("t1", "BAKKA", 100),
        MarketDataPoint("t2", "BAKKA", 100),
        MarketDataPoint("t3", "BAKKA", 97),
        MarketDataPoint("t4", "BAKKA", 102),
        MarketDataPoint("t4", "BAKKA", 100),
        MarketDataPoint("t4", "BAKKA", 101),
        MarketDataPoint("t4", "BAKKA", 100),
        MarketDataPoint("t4", "BAKKA", 100),
        MarketDataPoint("t4", "BAKKA", 108),
        MarketDataPoint("t4", "BAKKA", 109),# Should trigger a BUY signal
        MarketDataPoint("t4", "BAKKA", 110)  
    ]

    signals = []
    for t in ticks:
        signals.extend(strat.generate_signals(t))

    # Expect at least one BUY signal
    assert any(s["action"] == "BUY" for s in signals), "Expected a BUY signal for breakout"


def test_mean_reversion_strategy_signals_expected_behavior():
    """Confirm MeanReversionStrategy generates SELL when price exceeds mean by threshold."""

    strat = MeanReversionStrategy(lookback_window=3, threshold=0.01)

    ticks = [
        MarketDataPoint("t1", "ZTS", 100),
        MarketDataPoint("t2", "ZTS", 100),
        MarketDataPoint("t3", "ZTS", 100),
        MarketDataPoint("t4", "ZTS", 115),  # Should trigger a SELL signal
    ]

    signals = []
    for t in ticks:
        signals.extend(strat.generate_signals(t))

    # Expect at least one SELL signal due to overvaluation
    assert any(s["action"] == "SELL" for s in signals), "Expected a SELL signal for mean reversion"

