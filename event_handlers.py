from flask import render_template
from repo import Repo, Player
from slack_api import SlackApi
from event import Event

import event_handlers as handlers
import inspect


class EventHandler:
    def isMatch(event : Event):
        return False
    def handle(event : Event, repo: Repo, api : SlackApi):
        pass

class MakeMeMan(EventHandler):
    def isMatch(event : Event):
        return event.isPrivateMessageType() and event.text.lower().find('make me a man') > -1
    def handle(event : Event, repo: Repo, api : SlackApi):
        player = Player()
        player.username = event.sourceUser
        repo.savePlayer(player)

class AmIMan(EventHandler):
    def isMatch(event : Event):
        return event.isMentionType() and event.text.lower().find('am i a man?') > -1
    def handle(event : Event, repo: Repo, api : SlackApi):
        current = repo.getPlayerForUser(event.sourceUser)
        message = render_template('player.html', event=event, player=current)
        api.postToChat(event.sourceChannel, message)

class CallSomebody(EventHandler):
    def isMatch(event : Event):
        return event.isMentionType() and event.text.lower().find('call') > -1
    def handle(event : Event, repo: Repo, api : SlackApi):
        message = '<@' + event.sourceUser + '>, Call who a what now?'
        callIndex = event.text.lower().find('call')
        userStart = event.text.lower().find('<@', callIndex)
        userEnd = event.text.lower().find('>', callIndex)
        aIndex = event.text.lower().find(' a ', userEnd)
        if userStart > -1 and userEnd > -1 and aIndex > -1:
            target = event.text[userStart:userEnd+1].strip()
            what = event.text[aIndex+2:].strip()
            if len(target) > 0 and target == '<@'+event.sourceUser+'>':
                message = 'Sorry <@'+event.sourceUser+'>, that\'s fucked up.' 
            elif len(what) > 0 and len(target) > 0:
                message = target + ', you a ' + what + '.'
        api.postToChat(event.sourceChannel, message)



