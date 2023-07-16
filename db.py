import sqlite3

con = sqlite3.connect("whitelist.db")

def add_item(username, item):
    params = {
        "username": username,
        "item": item
    }
    with con:
        con.execute("INSERT INTO whitelist VALUES(:username, :item)", params)

def delete_item(username, item):
    params = { "username": username, "item": item }
    with con:
        con.execute("DELETE FROM whitelist WHERE username = :username AND item = :item", params)

def get_items(username):
    params = {
        "username": username
    }
    with con:
        return con.execute("SELECT item FROM whitelist WHERE username = :username", params).fetchall()

def init_database():
    with con:
        con.execute("DROP TABLE IF EXISTS whitelist")
        con.execute("CREATE TABLE whitelist(username, item)")
