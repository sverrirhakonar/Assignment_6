from abc import ABC, abstractmethod

class Observer(ABC):
    """Defines the interface for all observers."""
    @abstractmethod
    def update(self, signal: dict):
        pass


class SignalPublisher:
    """Publishes trading signals to attached observers."""

    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, signal: dict):
        for observer in self._observers:
            observer.update(signal)
