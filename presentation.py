
class Presenter:
    def username(username):
        if username == None or len(username) == 0:
            return ''
        return '<@' + username + '>'

    def player(player):
        if player == None:
            return ''

        return """You are a level """ + player.attributes.level + """ man.
Wallet: """+player.ozzyTokens+""" OTs
Experience: ("""+player.attributes.curExp+"""/"""+player.attributes.maxExp+""")
Health: ("""+player.attributes.curHp+"""/"""+player.attributes.max+""")""";
