import sqlite3

def get_player(playerName, server):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()
    
    playerInfo = cur.execute(
        "SELECT * FROM players WHERE name=? AND server=?", (playerName, server)).fetchone()
    playerTableNames = [description[0] for description in cur.description]

    
    if playerInfo == None:
        print("Player does not exist")
        create_player(playerName, server)
        print("Player Created")


    
    playerInfo = cur.execute(
        "SELECT * FROM players WHERE name=? AND server=?", (playerName, server)).fetchone()
    playerTableNames = [description[0] for description in cur.description]

    print(playerInfo)

    con.commit()
    con.close()

    player = dict(zip(playerTableNames, list(playerInfo)))

    return player


def get_player_by_id(playerId):
    con = sqlite3.connect('./database/playerTracker.db')

    cur = con.cursor()

    playerInfo = cur.execute("SELECT * FROM players WHERE id=?", (playerId,)).fetchone()
    playerTableNames = [description[0] for description in cur.description]

    con.commit()
    con.close()

    player = dict(zip(playerTableNames, list(playerInfo)))

    return player


def get_report_by_id(reportId):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()

    try:
        reportInfo = cur.execute("SELECT * FROM reports WHERE id=?", (reportId,)).fetchone()
        reportTableNames = [description[0] for description in cur.description]
        report = dict(zip(reportTableNames, list(reportInfo)))
        con.commit()
        con.close()
        return report
        
    
    except:    
        con.commit()
        con.close()
        return {'Error: ': 'No report found with that ID'}


def create_player(playerName, server):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()
    print(playerName, server)
    playerInfo = [playerName, server, 0, 0]
    cur.execute("INSERT INTO players(name, server, numberOfReports, numberOfCommendations) VALUES(?, ?, ?, ?)", playerInfo )

    con.commit()
    con.close()

    return {"Success: ": "Player Created Successfully"}


def countReports(playerId):
    return


def get_server(playerId):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()

    player = cur.execute("SELECT * FROM players WHERE id=?", (playerId,)).fetchone()
    playerServer = str(player.get('server'))
    
    serverInfo = cur.execute("SELECT * FROM servers WHERE name=?", (playerServer,)).fetchone()
    serverTableNames = [description[0] for description in cur.description]
    
    con.commit()
    con.close()

    server = dict(zip(serverTableNames, list(serverInfo)))

    return server


def get_player_rank(rankName):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()

    rankInfo = cur.execute(
        "SELECT * FROM ranks WHERE name=?", (rankName,)).fetchone()
    rankTableNames = [description[0] for description in cur.description]

    con.commit()
    con.close()

    rank = dict(zip(rankTableNames, list(rankInfo)))

    return rank


def get_commendations(playerId):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()

    playerReportsInfo = cur.execute("SELECT * FROM reports WHERE reportedId=? AND commendation=1", str(playerId),).fetchall()
    playerReportsTableNames = [description[0] for description in cur.description]

    con.commit()
    con.close()

    playerReports = []

    for reportInfo in playerReportsInfo:
        playerReports.append(dict(zip(playerReportsTableNames, reportInfo)))
    
    
    return playerReports


def get_reports(playerId, noOfReports = 0):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()
    print(noOfReports)
    playerReportsInfo = cur.execute("SELECT * FROM reports WHERE reportedId=? AND commendation=0", str(playerId),).fetchall()
    playerReportsTableNames = [description[0] for description in cur.description]

    con.commit()
    con.close()

    playerReports = []

    for reportInfo in playerReportsInfo:
        playerReports.append(dict(zip(playerReportsTableNames, reportInfo)))
    
    return playerReports


def create_report(report, reporterId):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()


    cur.execute("INSERT INTO reports(reportedBy, reportedId, reportedName, reportedCause, commendation, timeOfReport) VALUES(?, ?, ?, ?, ?, ?)", report)
    reportedId = str(report[1])
    reportIdentifiers = [str(report[4]), str(report[1])]

    numberOfReports = cur.execute("SELECT COUNT(*) FROM reports WHERE commendation=? AND reportedId=?", reportIdentifiers).fetchall()[0][0]
    playerReportUpdate = [numberOfReports, reportedId]
    cur.execute("UPDATE players SET numberOfReports=? WHERE id=?", playerReportUpdate)


    con.commit()
    con.close()
    print("report created")

    return {"Success: ": "Report Created Successfully"}

def get_user(reportedBy, reporterDiscordId):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor();

    userInfo = cur.execute(
        "SELECT * FROM users WHERE userName=? AND discordId=?", (reportedBy, reporterDiscordId)).fetchone()
    userTableNames = [description[0] for description in cur.description]

    
    if userInfo == None:
        print("User does not exist")
        create_user(reportedBy, reporterDiscordId)
        print("User Created")
    
    userInfo = cur.execute(
        "SELECT * FROM users WHERE userName=? AND discordId=?", (reportedBy, reporterDiscordId)).fetchone()
    userTableNames = [description[0] for description in cur.description]

    print(userInfo)

    con.commit()
    con.close()

    user = dict(zip(userTableNames, list(userInfo)))


    return user

def create_user(reportedBy, reporterDiscordId):
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()
    print(reportedBy, reporterDiscordId)
    userInfo = [reportedBy, reporterDiscordId]
    cur.execute("INSERT INTO users(userName, discordId) VALUES(?, ?)", userInfo )

    con.commit()
    con.close()

    return {"Success: ": "User Created Successfully"}

