#coding utf-8

import sqlite3
from datetime import datetime as dt

def logUser(userId): 
    conn = sqlite3.connect("data/bot.db")
    c = conn.cursor()
    query = "insert or replace into users(user_id, last_msg_time) values (?, ?)"

    lastMessageTime = dt.now().timestamp()
    c.execute(query, (str(userId), str(lastMessageTime)))
    conn.commit()
    
