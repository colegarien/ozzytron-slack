from db_util import DB

class Repo:
    def __init__(self):
        self.db = DB()

    def getPlayerForUser(self, username):
        row = self.db.selectOne("SELECT id, username, ozzy_tokens, level, exp, max_exp, hp, max_hp FROM player WHERE username = ?", [username])
        if row == None or len(row) == 0:
            return None

        player = Player()
        player.id = row['id']
        player.username = row['username']
        player.ozzyTokens = row['ozzy_tokens']

        player.attributes.level = row['level']
        player.attributes.curExp = row['exp']
        player.attributes.maxExp = row['max_exp']
        player.attributes.curHp = row['hp']
        player.attributes.maxHp = row['max_hp']

        return player

    def savePlayer(self, player):
        if player == None:
            return;

        currentPlayer = self.getPlayerForUser(player.username)
        if currentPlayer == None:
            player.id = self.db.insert("INSERT INTO player(username, ozzy_tokens, level, exp, max_exp, hp, max_hp) VALUES(?, ?, ?, ?, ?, ?, ?)", [player.username, player.ozzyTokens, player.attributes.level, player.attributes.curExp, player.attributes.maxExp, player.attributes.curHp, player.attributes.maxHp])
        else:
            self.db.insert("UPDATE player SET ozzy_tokens=?, level=?, exp=?, max_exp=?, hp=?, max_hp=? WHERE id=?", [player.ozzyTokens,player.attributes.level, player.attributes.curExp, player.attributes.maxExp, player.attributes.curHp, player.attributes.maxHp,player.id])
        return player

class Player:
    def __init__(self):
        self.id = None
        self.username = ''
        self.ozzyTokens = 20
        self.attributes = Attributes()

class Attributes:
    def __init__(self):
        self.level = 1
        self.curExp = 0
        self.maxExp = 10
        self.curHp = 20
        self.maxHp = 20
        

