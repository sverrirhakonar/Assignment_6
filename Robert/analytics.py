# analytics.py
import math
import pandas as pd
import numpy as np

class MetricsCapable:
    """Mixin interface: any wrapped object should respond to get_metrics()."""
    def get_metrics(self):
        # default: start with identity info if available
        out = {}
        if hasattr(self, "symbol"): out["symbol"] = self.symbol
        if hasattr(self, "price"):  out["price"] = self.price
        if hasattr(self, "issuer"): out["issuer"] = self.issuer
        return out


class InstrumentDecorator(MetricsCapable):
    """Base decorator: forwards attribute access to the wrapped instrument."""
    def __init__(self, instrument):
        self._instrument = instrument

    def __getattr__(self, item):
        # delegate unknown attributes/properties/methods to the wrapped object
        return getattr(self._instrument, item)

    def get_metrics(self):
        # start from underlying metrics if it defines them; else from mixin
        base = {}
        if hasattr(self._instrument, "get_metrics"):
            base = self._instrument.get_metrics()
        else:
            base = MetricsCapable.get_metrics(self._instrument)
        return dict(base)  # copy


# ---------- helpers (pure math; feed in price/return series you control) ----------

def _to_returns(price_series):
    s = pd.Series(price_series).astype(float)
    return s.pct_change().dropna()

def _stdev_annualized(returns, periods_per_year=252):
    r = pd.Series(returns).astype(float)
    if len(r) == 0:
        return None
    return float(r.std(ddof=1) * math.sqrt(periods_per_year))

def _beta(asset_returns, market_returns):
    a = pd.Series(asset_returns).astype(float).align(pd.Series(market_returns).astype(float), join="inner")[0]
    m = pd.Series(asset_returns).astype(float).align(pd.Series(market_returns).astype(float), join="inner")[1]
    a, m = a.dropna(), m.dropna()
    if len(a) < 2 or len(m) < 2:
        return None
    cov = np.cov(a, m, ddof=1)[0, 1]
    var = np.var(m, ddof=1)
    return float(cov / var) if var != 0 else None

def _max_drawdown(price_series):
    p = pd.Series(price_series).astype(float)
    if len(p) == 0:
        return None
    cummax = p.cummax()
    dd = (p / cummax - 1.0)
    return float(dd.min())  # negative number, e.g. -0.23 = -23%


# ---------- concrete decorators ----------

class VolatilityDecorator(InstrumentDecorator):
    def __init__(self, instrument, price_series, periods_per_year=252):
        super().__init__(instrument)
        self._price_series = price_series
        self._ppy = periods_per_year

    def get_metrics(self):
        m = super().get_metrics()
        ret = _to_returns(self._price_series)
        m["volatility_ann"] = _stdev_annualized(ret, periods_per_year=self._ppy)
        return m


class BetaDecorator(InstrumentDecorator):
    def __init__(self, instrument, price_series, market_price_series):
        super().__init__(instrument)
        self._asset_prices = price_series
        self._market_prices = market_price_series

    def get_metrics(self):
        m = super().get_metrics()
        a_ret = _to_returns(self._asset_prices)
        m_ret = _to_returns(self._market_prices)
        m["beta"] = _beta(a_ret, m_ret)
        return m


class DrawdownDecorator(InstrumentDecorator):
    def __init__(self, instrument, price_series):
        super().__init__(instrument)
        self._price_series = price_series

    def get_metrics(self):
        m = super().get_metrics()
        m["max_drawdown"] = _max_drawdown(self._price_series)
        return m
