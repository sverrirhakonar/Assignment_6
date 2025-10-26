from abc import ABC, abstractmethod
from collections import deque, defaultdict
from math import sqrt
from typing import Dict, Deque, List, Optional, Any
import json
from models import MarketDataPoint

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> List[Dict[str, Any]]:
        """Makes sure that the generate_signals method is implemented in the subclasses."""
        pass


class BreakoutStrategy(Strategy):
    """This is a Volatility Breakout Strategy."""

    def __init__(self, lookback_window: int = 15, threshold: float = 0.03):
        self.n = int(lookback_window)
        self.k = 1.0 + float(threshold)

        self.prev_price: Dict[str, float] = {}
        self.ret_win: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=self.n))
        self.sum_ret: Dict[str, float] = defaultdict(float)
        self.sum_sq: Dict[str, float] = defaultdict(float)

    def _std_prev(self, sym: str) -> Optional[float]:
        d = self.ret_win[sym]
        if len(d) < self.n:
            return None
        s = self.sum_ret[sym]
        ss = self.sum_sq[sym]
        m = s / self.n
        var = (ss - self.n * m * m) / (self.n - 1) if self.n > 1 else 0.0
        return sqrt(var) if var > 0 else 0.0

    def generate_signals(self, tick: MarketDataPoint) -> List[Dict[str, Any]]:
        sym = tick.symbol
        px = float(tick.price)
        ts = tick.timestamp

        if sym not in self.prev_price or self.prev_price[sym] <= 0:
            self.prev_price[sym] = px
            return []

        r = (px / self.prev_price[sym]) - 1.0
        std_prev = self._std_prev(sym)
        out: List[Dict[str, Any]] = []

        if std_prev is not None and std_prev > 0:
            up = self.k * std_prev
            dn = -up
            if r > up:
                out.append({"symbol": sym, "action": "BUY", "price": px, "timestamp": ts})
            elif r < dn:
                out.append({"symbol": sym, "action": "SELL", "price": px, "timestamp": ts})

        win = self.ret_win[sym]
        if len(win) == self.n:
            old = win[0]
            self.sum_ret[sym] -= old
            self.sum_sq[sym] -= old * old
        win.append(r)
        self.sum_ret[sym] += r
        self.sum_sq[sym] += r * r

        self.prev_price[sym] = px
        return out


class MeanReversionStrategy(Strategy):
    """This is a Mean Reversion Strategy."""

    def __init__(self, lookback_window: int = 20, threshold: float = 0.02):
        self.n = int(lookback_window)
        self.band = float(threshold)

        self.prices: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=self.n))
        self.sum_px: Dict[str, float] = defaultdict(float)
        self.sum_sq_px: Dict[str, float] = defaultdict(float)

    def _mean_std(self, sym: str) -> Optional[tuple]:
        d = self.prices[sym]
        if len(d) < self.n:
            return None
        s = self.sum_px[sym]
        ss = self.sum_sq_px[sym]
        m = s / self.n
        var = (ss - self.n * m * m) / (self.n - 1) if self.n > 1 else 0.0
        std = sqrt(var) if var > 0 else 0.0
        return m, std

    def generate_signals(self, tick: MarketDataPoint) -> List[Dict[str, Any]]:
        sym = tick.symbol
        px = float(tick.price)
        ts = tick.timestamp
        out: List[Dict[str, Any]] = []

        stats = self._mean_std(sym)
        if stats is not None:
            m, _ = stats
            upper = m * (1.0 + self.band)
            lower = m * (1.0 - self.band)
            if px < lower:
                out.append({"symbol": sym, "action": "BUY", "price": px, "timestamp": ts})
            elif px > upper:
                out.append({"symbol": sym, "action": "SELL", "price": px, "timestamp": ts})

        win = self.prices[sym]
        if len(win) == self.n:
            old = win[0]
            self.sum_px[sym] -= old
            self.sum_sq_px[sym] -= old * old
        win.append(px)
        self.sum_px[sym] += px
        self.sum_sq_px[sym] += px * px

        return out


def load_strategy_params(json_path: str) -> Dict[str, Dict[str, Any]]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
