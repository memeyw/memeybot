import sqlite3
import config
from sqlite3 import Error

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connectToDB(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The sql error '{e}' occured")

    return connection

def checkForTable(table, serverid):
    con = connectToDB(config.emojiDBPath + 'stats' + config.commandPrefix + str(serverid) + '.db')
    con.row_factory = dict_factory
    cursor = con.cursor()
    cursor.execute("select name from sqlite_master where type ='table' and name=?", (table,))
    data = cursor.fetchall()
    if not data:
        print("Table '{}' not found. Creating...".format(table))
        cursor.execute("create table emotes(emoteName, timesUsed)")
        con.commit()
