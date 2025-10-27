# In patterns/observer.py
from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def update(self, signal: dict):
        pass

class SignalPublisher:

    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        """Attaches (subscribes) an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Publisher: Attached observer {observer.__class__.__name__}")

    def detach(self, observer: Observer):
        """Detaches (unsubscribes) an observer."""
        try:
            self._observers.remove(observer)
            print(f"Publisher: Detached observer {observer.__class__.__name__}")
        except ValueError:
            print(f"Publisher: Observer {observer.__class__.__name__} was not attached.")

    def notify(self, signal: dict):
        for observer in self._observers:
            try:
                observer.update(signal)
            except Exception as e:
                print(f"Publisher: Error notifying observer {observer.__class__.__name__}: {e}")
            
