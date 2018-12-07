import sqlite3

DB = "english.sqlite3"

LETTERS = "abcdefghijklmnopqrstuvwxyz"

def create_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE commonwords (
        id integer PRIMARY KEY,
        value text NOT NULL UNIQUE
    )""")
    conn.commit()
    conn.close()

def populate_boggle():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    with open("words.common.txt", "r") as f:
        for line in f.readlines():
            stripped = line.lower().strip()
            if not any(k not in LETTERS for k in stripped):
                try:
                    c.execute("INSERT INTO commonwords (value) VALUES (?)", (stripped,))
                    print(stripped)
                except:
                    pass
    conn.commit()
    conn.close()