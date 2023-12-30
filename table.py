from sqlite3 import connect


class Table:
    def __init__(self, db):
        self.con = connect(db)
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Stations(id INTEGER PRIMARY KEY,
         name TEXT NOT NULL, link TEXT NOT NULL, genre TEXT NOT NULL, name_low TEXT NOT NULL);''')
        self.con.commit()

    def add(self, name, link, genre):
        self.cur.execute('''INSERT INTO Stations(name, link, genre, name_low) Values(?, ?, ?, ?)''', (name, link, genre,
                                                                                                      name.lower()))
        self.con.commit()

    def search(self, name='', genre=''):
        return self.cur.execute("""SELECT name, genre, id, link FROM Stations 
        WHERE name_low LIKE ? AND genre LIKE ?""", ('%' + name + '%', '%' + genre + '%')).fetchall()

    def delete(self, row_id):
        self.cur.execute('''DELETE FROM Stations WHERE id = ?''', row_id)
        self.con.commit()

    def del_table(self):
        self.cur.execute('''DROP TABLE Stations''')
        self.con.commit()
