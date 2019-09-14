from repo import Repo
from slack_api import SlackApi
from event import Event

import event_handlers as handlers
import inspect

class EventQueue:
    def __init__(self, repo: Repo, api : SlackApi):
        self.handlers = []
        for name, theClass in inspect.getmembers(handlers, inspect.isclass):
            if issubclass(theClass, handlers.EventHandler) and not theClass is handlers.EventHandler:
                self.handlers.append(theClass)
        self.repo = repo
        self.api = api

    def queue(self, event : Event):
        # process immediately
        self.processEvent(event)

    def processEvent(self, event : Event):
        for handler in self.handlers:
            if getattr(handler, 'isMatch')(event):
                getattr(handler, 'handle')(event, self.repo, self.api)
                return True
        if not event.isPrivateMessageType() and event.isMentionType():
            message = 'Sorry <@' + event.sourceUser + '>, I\'mma damn retard!'
            self.api.postToChat(event.sourceChannel, message)
        return False



