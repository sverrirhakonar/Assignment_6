# Assignment_6

Design Patterns in Financial Software Architecture

## Setup Instructions

1. **Prepare your environment.**Use Python 3.10 or newer.
2. **Run the program.**

   ```bash
   python main.py
   ```

**
    3. See the results.**

    The console will show strategy signals, observer logs, and trade actions.

## Module Descriptions

* **data_loader.py**

  Loads market data from CSV, JSON, or XML and converts to internal format.
* **models.py**

  Has `MarketDataPoint`, `Position`, `Portfolio`, and `Broker` classes.
* **analytics.py**

  Adds analytics like volatility, beta, and drawdown with decorators.
* **patterns/**

  Contains all design patterns:

  * `factory.py` — Makes instrument objects
  * `singleton.py` — Global config
  * `builder.py` — Builds portfolio structure
  * `strategy.py` — Breakout and MeanReversion strategies
  * `observer.py` — Logger and Alert observers
  * `command.py` — Executes trades and supports undo/redo
* **engine.py**

  Runs strategies, processes ticks, and signals.
* **reporting.py**

  Handles logging and alert messages.
* **tests/**

  Small tests.
* **design_report.md**

  Short report about patterns, rationale, and tradeoffs.


### References:

1. ChatGPT 5, used to help with coding, ask questions about design patterns, why to implement a certain way, etc.
2. Cursor, tab feature that uses a couple AI models.
3. Sverrir Hakonarson and Robert Asgeirsson (Old code from past projects).
4. Course slides.
