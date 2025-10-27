import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from patterns.Command import ExecuteOrderCommand, CommandInvoker
from models import Broker

def test_command_execute_undo_redo():
    broker = Broker(starting_cash=10_000.0)
    invoker = CommandInvoker()

    order = {
        "timestamp": "t1",
        "symbol": "ADBE",
        "side": "BUY",
        "qty": 10,
        "price": 100.0,
    }

    cmd = ExecuteOrderCommand(broker, order)

    # Execute
    invoker.do(cmd)
    after_exec = broker.summary()
    assert after_exec["cash"] == 9000.0
    # One position with qty 10
    positions = {p["symbol"]: p for p in after_exec["positions"]}
    assert positions["ADBE"]["qty"] == 10

    # Undo
    invoker.undo()
    after_undo = broker.summary()
    assert after_undo["cash"] == 10_000.0
    # Flat position list or no ADBE position
    positions_after_undo = {p["symbol"]: p for p in after_undo["positions"]}
    assert "ADBE" not in positions_after_undo

    # Redo
    invoker.redo()
    after_redo = broker.summary()
    assert after_redo["cash"] == 9000.0
    positions_after_redo = {p["symbol"]: p for p in after_redo["positions"]}
    assert positions_after_redo["ADBE"]["qty"] == 10