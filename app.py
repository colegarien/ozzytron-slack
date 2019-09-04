from flask import Flask, jsonify, make_response, request, abort
import requests
from db_util import DB

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('ozzytron.cfg', silent=True)

db = DB()

@app.route('/', methods=['POST', 'GET'])
def index():
    content = request.get_json()
    if content != None and content['type'] == 'url_verification':
        return jsonify({'challenge' : content['challenge']})
    elif content != None and content['event']['type'] == 'app_mention':
       handleMention(content) 
    elif content != None and content['event']['type'] == 'message' and content['event']['channel_type'] == 'im':
        handlePrivateMessage(content)
    elif content != None:
        print(content['event']['type'])

    return jsonify({'success':True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

def handlePrivateMessage(content):
    user = content['event']['user']
    channel = content['event']['channel']
    text = content['event']['text']
    if text.find('make me a man') > -1:
        current = db.selectOne("SELECT id FROM player WHERE username = ?", [user])
        if current == None or len(current) == 0:
            print ('none')
            db.insert("INSERT INTO player(username, ozzy_tokens) VALUES(?, ?)", [user, 20])


def handleMention(content):
    user = content['event']['user']
    channel = content['event']['channel']
    text = content['event']['text']
    if text.find('am I a man?') > -1:
        current = db.selectOne("""SELECT id, ozzy_tokens FROM player WHERE username = ?""", [user])
        if current == None:
            message = 'No <@'+user+'>. No you are not.'
        else:
            message = 'Yes <@'+user+'>! You are man ' + str(current['id']) + '. Your wallet currently has '+str(current['ozzy_tokens'])+' OTs' 
    elif text.find('call') > -1:
        message = '<@' + user + '>, Call who a what now?'
        callIndex = text.find('call')
        userStart = text.find('<@', callIndex)
        userEnd = text.find('>', callIndex)
        aIndex = text.find(' a ', userEnd)
        if userStart > -1 and userEnd > -1 and aIndex > -1:
            target = text[userStart:userEnd+1].strip()
            what = text[aIndex+2:].strip()
            if len(target) > 0 and target == '<@'+user+'>':
                message = 'Sorry <@'+user+'>, that\'s fucked up.' 
            elif len(what) > 0 and len(target) > 0:
                message = target + ', you a ' + what + '.'
    elif text.find('add') > -1:
        message = '<@' + user + '>, Add what?'
        what = text[text.find('add')+3:].strip()
        if len(what) > 0:
            pass # TODO save to sqlite db
    elif text.find('show') > -1:
        message = '<@' + user + '>' + ', show you what?'
        # TODO pull the added stuff
    else:
        message = 'Sorry <@' + user + '>, I\'mma damn retard!'
    postToChat(channel, message)

def getSlackApiHeaders():
    return {'Content-Type' : 'application/json; charset=utf-8', 'Authorization' : 'Bearer ' + app.config['BOT_OAUTH'] }

def postToChat(channel, message):
    chatUrl = app.config['BASE_SLACK_API'] + 'chat.postMessage'
    headers = getSlackApiHeaders()
    data = {'channel' : channel, 'text' : message, 'as_user' : True}
    requests.post(chatUrl, json=data, headers=headers)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
