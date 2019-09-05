from flask import Flask, jsonify, make_response, request, abort
import requests
from repo import Repo, Player

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('ozzytron.cfg', silent=True)

repo = Repo()

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

class EventHandler:
    def isMatch(event : Event):
        return False
    def handle(event : Event):
        pass

class MakeMeMan(EventHandler):
    def isMatch(event : Event):
        return event.isPrivateMessageType() and event.text.find('make me a man') > -1
    def handle(event : Event):
        player = Player()
        player.username = event.sourceUser
        repo.savePlayer(player)

class AmIMan(EventHandler):
    def isMatch(event : Event):
        return event.isMentionType() and event.text.find('am I a man?') > -1
    def handle(event : Event):
        current = repo.getPlayerForUser(event.sourceUser)
        if current == None:
            message = 'No <@'+event.sourceUser+'>. No you are not.'
        else:
            message = 'Yes <@'+event.sourceUser+'>! You are man ' + str(current.id) + '. Your wallet currently has '+str(current.ozzyTokens)+' OTs' 
        postToChat(event.sourceChannel, message)

class CallSomebody(EventHandler):
    def isMatch(event : Event):
        return event.isMentionType() and event.text.find('call') > -1
    def handle(event : Event):
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
        postToChat(event.sourceChannel, message)

eventHandlers = ['MakeMeMan', 'AmIMan', 'CallSomebody']

@app.route('/', methods=['POST', 'GET'])
def index():
    content = request.get_json()
    if content != None and content['type'] == 'url_verification':
        return jsonify({'challenge' : content['challenge']})
    elif content != None:
        processEvent(eventHandlers, Event.fromRequest(content))

    return jsonify({'success':True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


def processEvent(handlers, event):
    for handlerClass in handlers:
        handler = globals()[handlerClass]
        if getattr(handler, 'isMatch')(event):
            getattr(handler, 'handle')(event)
            return True
    message = 'Sorry <@' + event.sourceUser + '>, I\'mma damn retard!'
    postToChat(event.sourceChannel, message)
    return False

def getSlackApiHeaders():
    return {'Content-Type' : 'application/json; charset=utf-8', 'Authorization' : 'Bearer ' + app.config['BOT_OAUTH'] }

def postToChat(channel, message):
    chatUrl = app.config['BASE_SLACK_API'] + 'chat.postMessage'
    headers = getSlackApiHeaders()
    data = {'channel' : channel, 'text' : message, 'as_user' : True}
    requests.post(chatUrl, json=data, headers=headers)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
