from db_util import DB

class Repo:
    def __init__(self):
        self.db = DB()

    def getPlayerForUser(self, username):
        row = self.db.selectOne("SELECT id, username, ozzy_tokens FROM player WHERE username = ?", [username])
        if row == None or len(row) == 0:
            return None

        player = Player()
        player.id = row['id']
        player.username = row['username']
        player.ozzyTokens = row['ozzy_tokens']
        return player

    def savePlayer(self, player):
        if player == None:
            return;

        currentPlayer = self.getPlayerForUser(player.username)
        if currentPlayer == None:
            player.id = self.db.insert("INSERT INTO player(username, ozzy_tokens) VALUES(?, ?)", [player.username, player.ozzyTokens])
        else:
            self.db.insert("UPDATE player SET ozzy_tokens=? WHERE id=?", [player.ozzyTokens, player.id])
        return player

class Player:
    def __init__(self):
        self.id = None
        self.username = ''
        self.ozzyTokens = 20
