import sqlite3

def create_database():
    
    con = sqlite3.connect('./database/playerTracker.db')
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS ranks(
                id integer primary key autoincrement,
                name text not null,
                description text not null
            );
    ''')

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS players(
                id integer primary key autoincrement,
                name text not null,
                server text not null,
                numberOfReports integer not null,
                numberOfCommendations integer not null
            );
    ''')

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS reports(
                id integer primary key autoincrement,
                reporterId integer not null,
                reportedId integer not null,
                reportedName text not null,
                reportedCause text not null,
                commendation integer not null,
                timeOfReport text not null
            );    
    ''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS servers(
                id integer primary key autoincrement,
                name text not null
        );
    ''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS users(
                id integer primary key autoincrement,
                userName text not null,
                discordId text not null
        );
    ''')