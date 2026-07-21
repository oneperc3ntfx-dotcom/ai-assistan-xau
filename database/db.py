import sqlite3


conn = sqlite3.connect(
    "members.db",
    check_same_thread=False
)


cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS members(

id INTEGER PRIMARY KEY AUTOINCREMENT,

telegram_id TEXT,

username TEXT,

name TEXT,

package TEXT,

expired TEXT,

status TEXT

)

""")


conn.commit()
