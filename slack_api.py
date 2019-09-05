import requests

class SlackApi:
    def __init__(self, baseUrl, botToken):
        self.baseUrl = baseUrl
        self.botToken = botToken

    def getSlackApiHeaders(self):
        return {'Content-Type' : 'application/json; charset=utf-8', 'Authorization' : 'Bearer ' + self.botToken }

    def postToChat(self, channel, message):
        chatUrl = self.baseUrl + 'chat.postMessage'
        headers = self.getSlackApiHeaders()
        data = {'channel' : channel, 'text' : message, 'as_user' : True}
        requests.post(chatUrl, json=data, headers=headers)


