from repo import Repo
from slack_api import SlackApi
from event import Event

import threading
import event_handlers as handlers
import inspect
import time

class EventQueue:
    def __init__(self, repo: Repo, api : SlackApi):
        self.handlers = []
        for name, theClass in inspect.getmembers(handlers, inspect.isclass):
            if issubclass(theClass, handlers.EventHandler) and not theClass is handlers.EventHandler:
                self.handlers.append(theClass)
        self.repo = repo
        self.api = api
        
        # thread for processing events
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.eventQueue = []

    def run(self):
        while True:
            if len(self.eventQueue) > 0:
                # process events
                self.processEvent(self.eventQueue.pop())
            time.sleep(2)

    def queue(self, event : Event):
        if not self.thread.isAlive():
            self.thread.start()
        # queue it for later
        self.eventQueue.append(event)

    def processEvent(self, event : Event):
        for handler in self.handlers:
            if getattr(handler, 'isMatch')(event):
                getattr(handler, 'handle')(event, self.repo, self.api)
                return True
        if not event.isPrivateMessageType() and event.isMentionType():
            message = 'Sorry <@' + event.sourceUser + '>, I\'mma damn retard!'
            self.api.postToChat(event.sourceChannel, message)
        return False



