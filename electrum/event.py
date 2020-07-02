
from collections import defaultdict

class Event:
    """Event Class manage event and callbacks.
    """
    __instance = None

    def __init__(self):
        if Event.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Event.__instance = self

        self.callbacks = defaultdict(list)

        
     
    @staticmethod 
    def getInstance():
      """ Static access method. """
      if Event.__instance == None:
         Event()
      return Event.__instance

    def register_callback(self, callback, events):
            for event in events:
                self.callbacks[event].append(callback)

    def unregister_callback(self, callback):
            for callbacks in self.callbacks.values():
                if callback in callbacks:
                    callbacks.remove(callback)

    def trigger_callback(self, event, *args):
        callbacks = self.callbacks[event][:]
        for callback in callbacks:
                callback(event, *args)
            