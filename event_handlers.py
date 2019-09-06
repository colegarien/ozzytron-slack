from repo import Repo, Player
from slack_api import SlackApi

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


class EventQueue:
    def __init__(self, repo: Repo, api : SlackApi):
        self.handlers = [MakeMeMan, AmIMan, CallSomebody]
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
        message = 'Sorry <@' + event.sourceUser + '>, I\'mma damn retard!'
        self.api.postToChat(event.sourceChannel, message)
        return False



class EventHandler:
    def isMatch(event : Event):
        return False
    def handle(event : Event, repo: Repo, api : SlackApi):
        pass

class MakeMeMan(EventHandler):
    def isMatch(event : Event):
        return event.isPrivateMessageType() and event.text.find('make me a man') > -1
    def handle(event : Event, repo: Repo, api : SlackApi):
        player = Player()
        player.username = event.sourceUser
        repo.savePlayer(player)

class AmIMan(EventHandler):
    def isMatch(event : Event):
        return event.isMentionType() and event.text.find('am I a man?') > -1
    def handle(event : Event, repo: Repo, api : SlackApi):
        current = repo.getPlayerForUser(event.sourceUser)
        if current == None:
            message = 'No <@'+event.sourceUser+'>. No you are not.'
        else:
            message = 'Yes <@'+event.sourceUser+'>! You are man ' + str(current.id) + '. Your wallet currently has '+str(current.ozzyTokens)+' OTs' 
        api.postToChat(event.sourceChannel, message)

class CallSomebody(EventHandler):
    def isMatch(event : Event):
        return event.isMentionType() and event.text.find('call') > -1
    def handle(event : Event, repo: Repo, api : SlackApi):
        message = '<@' + event.sourceUser + '>, Call who a what now?'
        callIndex = event.text.find('call')
        userStart = event.text.find('<@', callIndex)
        userEnd = event.text.find('>', callIndex)
        aIndex = event.text.find(' a ', userEnd)
        if userStart > -1 and userEnd > -1 and aIndex > -1:
            target = event.text[userStart:userEnd+1].strip()
            what = event.text[aIndex+2:].strip()
            if len(target) > 0 and target == '<@'+event.sourceUser+'>':
                message = 'Sorry <@'+event.sourceUser+'>, that\'s fucked up.' 
            elif len(what) > 0 and len(target) > 0:
                message = target + ', you a ' + what + '.'
        api.postToChat(event.sourceChannel, message)



