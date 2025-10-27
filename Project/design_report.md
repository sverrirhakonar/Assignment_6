# Assignment_6

Design Patterns in Financial Software Architecture

## Summary of Patterns Used

- **Factory Pattern**
  - Creates instrument objects (Stock, Bond, ETF) from data dynamically.
- **Singleton Pattern**
  - Ensures shared configuration across modules.
- **Builder Pattern**
  - Builds nested portfolio structures step-by-step.
- **Decorator Pattern**
  - Adds analytics (volatility, beta, drawdown) without altering base classes.
- **Adapter Pattern**
  - Converts external data formats (JSON, XML) to internal MarketDataPoint objects.
- **Composite Pattern**
  - Aggregates positions and sub-portfolios hierarchically.
- **Strategy Pattern**
  - Provides interchangeable trading strategies (MeanReversion, Breakout).
- **Observer Pattern**
  - Notifies modules (loggers, alerts) when signals are generated.
- **Command Pattern**
  - Encapsulates order execution and supports undo/redo for trades.


## Rationale

It becomes easier to change, test, and add new parts later.
Each pattern keeps the code more clean and not all mixed.
It takes a few more files, but the structure is clearer and the program is more stable.

## Tradeoffs

There is a bit more code and maybe harder to understand in the beginning,
but later it saves time because new features can be added or changed easier.
