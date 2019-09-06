from event_handlers import EventQueue, Event, EventHandler
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

if __name__ == '__main__':
    unittest.main()
