class Event:
    def fromRequest(request):
        eventData = request.get('event', {})
        event = Event(eventData.get('user',''),eventData.get('channel',''),eventData.get('text',''),eventData.get('type', 'none'),eventData.get('channel_type','normal'))
        return event
    
    def __init__(self, user, channel, text, eventType, channelType):
        self.sourceUser = user
        self.sourceChannel = channel
        self.text = text
        self.eventType = eventType
        self.channelType = channelType

    def isEmpty(self):
        return self.eventType == 'none'

    def isMentionType(self):
        return self.eventType == 'app_mention'
        
    def isPrivateMessageType(self):
        return self.eventType == 'message' and self.channelType == 'im'

