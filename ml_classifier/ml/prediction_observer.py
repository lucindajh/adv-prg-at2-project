class PredictionObserver:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, func):
        self.subscribers.append(func)

    def update(self, info):
        for func in self.subscribers:
            func(info)
