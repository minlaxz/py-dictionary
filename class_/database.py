import sqlite3


class DB:
    def __init__(self, table):
        self.table_name = table
        self.limit = 30

        self.db = sqlite3.connect('assets/dictionary.sqlite')
        self.cur = self.db.cursor()
        self.create_table()

    def create_table(self):

        sql = f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY,english TEXT,myanmar TEXT)'
        self.cur.execute(sql)
        # commit
        self.db.commit()

    def findAll(self, limit=None):
        if limit == None:
            limit = self.limit
        sql = f"SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT ?"
        self.cur.execute(sql, (limit,))
        return self.cur.fetchall()

    # db close
    def __del__(self):
        self.db.close()


class Dict(DB):
    def __init__(self):
        super().__init__('dictionary')

    def add(self, eng, mm):
        sql = f'INSERT INTO {self.table_name} (english,myanmar) VALUES (?,?)'
        self.cur.execute(sql, (eng, mm))
        self.db.commit()

    def search_eng(self, word):
        sql = f"SELECT * FROM {self.table_name} WHERE english LIKE ? LIMIT ?"
        self.cur.execute(sql, (f"{word}%", self.limit))
        return self.cur.fetchall()

    def search_mm(self, word):
        sql = f"SELECT * FROM {self.table_name} WHERE myanmar LIKE ? LIMIT ?"
        self.cur.execute(sql, (f"%{word}%", self.limit))
        return self.cur.fetchall()


class History(DB):
    def __init__(self):
        super().__init__('history')

    def create_table(self):
        sql = f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY,name TEXT UNIQUE)'
        self.cur.execute(sql)
        self.db.commit()

    def add(self, name):
        sql = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cur.execute(sql, (name,))
        self.db.commit()

    def deleteById(self, id):
        sql = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cur.execute(sql, (id,))
        self.db.commit()

    def deleteAll(self):
        sql = f"DELETE FROM {self.table_name}"
        self.cur.execute(sql)
        self.db.commit()
