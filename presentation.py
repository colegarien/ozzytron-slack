
class Presenter:
    def username(username):
        if username == None or len(username) == 0:
            return ''
        return '<@' + username + '>'

    def player(player):
        if player == None:
            return '...'

        return 'You are a level {} man.\nWallet: {} OTs\nExperience: ({}/{})\nHealth: ({}/{})'.format(player.attributes.level,player.ozzyTokens,player.attributes.curExp,player.attributes.maxExp,player.attributes.curHp,player.attributes.maxHp)
