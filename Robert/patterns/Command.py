class Command:
    def execute(self):
        pass
    def undo(self):
        pass

class ExecuteOrderCommand(Command):
    def __init__(self, broker, order):
        self.broker = broker
        self.order = order
        self.executed = False

    def execute(self):
        if not self.executed:
            self.broker.execute_order(
                self.order["symbol"],
                self.order["side"],
                self.order["qty"],
                self.order["price"]
            )
            self.executed = True

    def undo(self):
        if self.executed:
            reverse = dict(self.order)
            reverse["side"] = "SELL" if self.order["side"] == "BUY" else "BUY"
            self.broker.execute_order(
                reverse["symbol"],
                reverse["side"],
                reverse["qty"],
                reverse["price"]
            )
            self.executed = False

class CommandInvoker:
    def __init__(self):
        self.done = []
        self.undone = []

    def do(self, cmd: Command):
        cmd.execute()
        self.done.append(cmd)
        self.undone.clear()

    def undo(self):
        if self.done:
            cmd = self.done.pop()
            cmd.undo()
            self.undone.append(cmd)

    def redo(self):
        if self.undone:
            cmd = self.undone.pop()
            cmd.execute()
            self.done.append(cmd)
