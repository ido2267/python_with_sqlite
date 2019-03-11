import sqlite3 as sq3


def connect():
    conn=sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("CREATE TABLE IF NOT EXISTS book(id INTEGRER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER) ")
    conn.commit( )
    conn.close()

def get_last_id():
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("SELECT id FROM book ORDER BY id DESC")
    rows = curr.fetchall()
    print (rows)
    id = int(rows[0][0])
    conn.close()
    return id

def insert(title,author,year,isbn):
    id=get_last_id() +1
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("INSERT INTO book VALUES (?,?,?,?,?)",(id,title,author,year,isbn))
    conn.commit( )
    conn.close()

def view():
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM book")
    rows = curr.fetchall()
    conn.close()
    return rows


def delete_by_title (title):
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("DELETE FROM book WHERE title=?",(title,))
    conn.commit( )
    conn.close()

def search(title="",author="",year="",isbn=""):
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",(title,author,year,isbn))
    rows = curr.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    curr.execute("DELETE FROM book WHERE id=?",(id,))
    conn.commit()
    conn.close()

def update(id,title,author,year,isbn):
    conn = sq3.connect("books.db")
    curr = conn.cursor()
    # curr.execute("UPDATE book SET id=? WHERE title=? AND author=? AND year=? AND isbn=?",(id,title,author,year,isbn))
    curr.execute("UPDATE book SET  title=? AND author=? AND year=? AND isbn=? WHERE  id=?",
                 (title, author, year, isbn,id))
    conn.commit( )
    conn.close()


connect()