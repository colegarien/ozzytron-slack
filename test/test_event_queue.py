from app import app
from event_queue import EventQueue
from event_handlers import EventHandler
from event import Event
import unittest
from unittest import mock

class NonMatchingEventHandler(EventHandler):
    def isMatch(event : Event):
        return False
    def handle(event, repo, api):
        pass

class MatchingEventHandler(EventHandler):
    def isMatch(event : Event):
        return True
    def handle(event, repo, api):
        pass

class TestEventQueue(unittest.TestCase):

    def setUp(self):
        self.api = mock.MagicMock()
        self.repo = mock.MagicMock()

    def test_processEvent_emptyEvent_returnFalse(self):
        # Arrange
        queue = EventQueue(self.repo, self.api)
        queue.handlers = [ NonMatchingEventHandler ]

        event = Event.fromRequest({})
        
        # Act
        actual = queue.processEvent(event)

        # Assert
        self.assertFalse(actual)

    def test_processEvent_matchedEvent_returnTrue(self):
        # Arrange
        queue = EventQueue(self.repo, self.api)
        queue.handlers = [ MatchingEventHandler ]

        event = Event.fromRequest({})
        
        # Act
        actual = queue.processEvent(event)

        # Assert
        self.assertTrue(actual)

    def test_processEvent_MakeMeManHandler_savePlayer(self):
        # Arrange
        queue = EventQueue(self.repo, self.api)
        event = Event.fromRequest({'event' : {'text' : 'make me a man', 'type': 'message', 'channel_type' : 'im'}})

        # Act
        actual = queue.processEvent(event)

        # Assert
        self.assertTrue(actual)

    def test_processEvent_AmIMan_postMessage(self):
        # Arrange
        queue = EventQueue(self.repo, self.api)
        event = Event.fromRequest({'event' : {'text' : 'am I a man?', 'type': 'app_mention'}})

        # Act
        with app.app_context():
            actual = queue.processEvent(event)

        # Assert
        self.assertTrue(actual)

    def test_processEvent_CallSomebody_postMessage(self):
        # Arrange
        queue = EventQueue(self.repo, self.api)
        event = Event.fromRequest({'event' : {'text' : 'call <@something> a bitch', 'type': 'app_mention'}})

        # Act
        actual = queue.processEvent(event)

        # Assert
        self.assertTrue(actual)


if __name__ == '__main__':
    unittest.main()
