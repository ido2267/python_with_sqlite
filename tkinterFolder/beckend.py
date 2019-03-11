import sqlite3 as sq3

class Library():
    def __init__(self,db):
        self.conn=sq3.connect(db)
        self.curr = self.conn.cursor()
        books_sql = "CREATE TABLE IF NOT EXISTS book(id INTEGRER PRIMARY KEY, title TEXT NOT NULL," \
                    " author TEXT NOT NULL, pages INTEGER NOT NULL) "
        self.curr.execute(books_sql)
        shelves_sql = "CREATE TABLE IF NOT EXISTS shelves(letter CHAR (1) NOT NULL, shelve_id INTEGER NOT NULL" \
                      " UNIQUE(letter, shelve_id) ON CONFLICT REPLACE) "
        self.curr.execute(shelves_sql)
        books_on_shelves = "CREATE TABLE IF NOT EXISTS books_on_shelves(letter CHAR (1) NOT NULL, shelve_id INTEGER NOT NULL " \
                           "FOREIGN KEY(letter,shelve_id) REFERENCES shelves(letter,shelve_id)"  \ 
                           " book_id INTEGRER NOT NULL REFERENCES book(id) )"
        self.curr.execute(books_on_shelves)

        self.conn.commit( )
    def get_last_id(self):
        self.curr.execute("SELECT id FROM book ORDER BY id DESC")
        rows = self.curr.fetchall()
        print (rows)
        id = int(rows[0][0])
        return id
    def insert(self,title,author,year,isbn):
        id = self.get_last_id()
        id +=1
        self.curr.execute("INSERT INTO book VALUES (?,?,?,?,?)",(id,title,author,year,isbn))
        self.conn.commit( )
    def view(self):
        self.curr.execute("SELECT * FROM book")
        rows = self.curr.fetchall()
        return rows
    def delete_by_title (self,title):
        self.curr.execute("DELETE FROM book WHERE title=?",(title,))
        self.conn.commit( )
    def search(self,title="",author="",year="",isbn=""):
        self.curr.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",(title,author,year,isbn))
        rows = self.curr.fetchall()
        return rows
    def delete(self,id):
        self.curr.execute("DELETE FROM book WHERE id=?",(id,))
        self.conn.commit()
    def update(self,id,title,author,year,isbn):
        self.curr.execute("UPDATE book SET  title=? AND author=? AND year=? AND isbn=? WHERE  id=?",
                     (title, author, year, isbn,id))
        self.conn.commit( )
    def __del__(self):
        self.conn.close()
