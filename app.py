from flask import Flask, jsonify, make_response, request, abort
from repo import Repo
from slack_api import SlackApi
from event_queue import EventQueue
from event import Event

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('ozzytron.cfg', silent=True)

api = SlackApi(app.config['BASE_SLACK_API'],app.config['BOT_OAUTH'])
repo = Repo()
eventQueue = EventQueue(repo, api)

@app.route('/', methods=['POST', 'GET'])
def index():
    content = request.get_json()
    if content != None and content['type'] == 'url_verification':
        return jsonify({'challenge' : content['challenge']})
    elif content != None:
        eventQueue.queue(Event.fromRequest(content))
    return jsonify({'success':True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
