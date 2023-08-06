class Observable:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        if observer in self.observers:
            raise Exception("this observer is already registered.")

        self.observers.append(observer)

    async def _notify_observers(self):
        for observer in self.observers:
            await observer.notify(self)
