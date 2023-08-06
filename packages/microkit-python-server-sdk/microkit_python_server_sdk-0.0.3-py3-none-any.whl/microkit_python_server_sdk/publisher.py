

import uuid

class Publisher:
    
    def __init__(self):
        self.subscribers = {}

    def subscribe (self, func):
        key = str(uuid.uuid4())
        self.subscribers[key] = func
        return Subscription(self, key)
    
    def unsubscribe (self, key):
        self.subscribers.pop(key, None)
    
    def call (self, key):
        self.subscribers[key]()
    
    def publish (self, currentValue, prevValue):
        for key, callback in self.subscribers.items():
            callback(currentValue, prevValue)



class Subscription:
    def __init__(self, publisher, key):
        self.publisher = publisher
        self.key = key

    def unsubscribe(self):
        self.publisher.unsubscribe(self.key)
    
    def call(self):
        self.publisher.call(self.key)