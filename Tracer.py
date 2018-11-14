#coding utf-8

import sqlite3
from datetime import datetime as dt
import ApiGate

def logUser(userId): 
    conn = sqlite3.connect("data/bot.db")
    c = conn.cursor()
    query = "insert or replace into users(user_id, last_msg_time, full_name) values (?, ?, ?)"

    user = ApiGate.getUser(userId)

    lastMessageTime = dt.now().timestamp()
    fullName = user["first_name"] + " " + user["last_name"]


    params = (
        str(userId), 
        str(lastMessageTime),
        fullName
    )

    c.execute(query, params)
    conn.commit()
