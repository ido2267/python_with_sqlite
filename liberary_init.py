import sqlite3 as sq3
import book as bk

shelf_size = 150
file_name = "bookdatabase.txt"
class Init_Library():
    def __init__(self,db):
        _shelves_allwoed = 1000

        self.conn=sq3.connect(db)
        self.curr = self.conn.cursor()
        books_sql = "CREATE TABLE IF NOT EXISTS book(book_id INTEGRER PRIMARY KEY, title TEXT NOT NULL," \
                    " author TEXT NOT NULL, pages INTEGER NOT NULL) "
        self.curr.execute(books_sql)
        shelves_sql = "CREATE TABLE IF NOT EXISTS shelves(letter CHAR (1) NOT NULL, shelf_id INTEGER NOT NULL," \
                      " PRIMARY KEY(letter, shelf_id) ) "
        self.curr.execute(shelves_sql)
        books_on_shelves = "CREATE TABLE IF NOT EXISTS books_on_shelves(letter CHAR (1) NOT NULL, shelf_id INTEGER NOT NULL ," \
                           "book_id INTEGRER NOT NULL REFERENCES book (book_id),FOREIGN KEY(letter,shelf_id) REFERENCES shelves )"
        self.curr.execute(books_on_shelves)
        reader_sql = "CREATE TABLE IF NOT EXISTS readers(name TEXT NOT NULL, books_allowed INTEGER NOT NULL," \
                     " reader_id INTEGER) "
        self.curr.execute(reader_sql)

        books_for_readers = "CREATE TABLE IF NOT EXISTS books_for_readers(reader_id INTEGRER NOT NULL REFERENCES readers(reader_id)," \
                            " book_id INTEGRER NOT NULL REFERENCES book(book_id), date_borrowed CHAR(10))"
        self.curr.execute(books_for_readers)

        with open(file_name, "r") as book_database:
            book_load_sql = "INSERT INTO book (book_id,title, author,pages) VALUES (?, ?,?,?)"
            buffer = book_database.read()
            arr = buffer.split('\n')
            for book_id in range(0, len(arr) -1):
                if arr[book_id]:
                    bookName, writer, pages =  arr[book_id].split(',')
                    pages = int(pages)
                    self.curr.execute(book_load_sql,(book_id,bookName, writer, pages))
                    self.place_book_on_shelf(book_id)
        # books = self.view_books()
        # for book in books:
        #     book_id = book[0]

        self.conn.commit( )

    def get_last_id(self, sql_str):
        self.curr.execute(sql_str)
        rows = self.curr.fetchall()
        if rows:
            id = int(rows[0][0])
        else:
            id = 0
        return id

    def get_last_book_id(self):
        sql_str ="SELECT IFNULL(book_id,0) FROM book ORDER BY book_id DESC"
        return self.get_last_id(sql_str)

    def get_last_reader_id(self):
        sql_str ="SELECT IFNULL(reader_id,0) FROM readers ORDER BY reader_id DESC"
        return self.get_last_id(sql_str)

    def get_last_shelf_id(self,letter):
        sql_str = "SELECT count(*) FROM shelves  WHERE letter = '{}' ".format(letter)
        result = self.get_last_id(sql_str)
        if result > 0 :
            sql_str = "SELECT IFNULL(shelf_id,0) FROM shelves  WHERE letter = '{}' ORDER BY shelf_id DESC".format(letter)
            result = self.get_last_id(sql_str)
        else:
            result = 1
        return result

    def add_new_book(self,title,author,pages):
        id = self.get_last_book_id()
        id +=1
        self.curr.execute("INSERT INTO book VALUES (?,?,?,?)",(id,title,author,pages))
        self.conn.commit( )
        return id

    def add_new_reader(self, name, books_allowed=2):
        id = self.get_last_reader_id()
        id += 1
        self.curr.execute("INSERT INTO readers VALUES (?,?,?)", (name, books_allowed, id))
        self.conn.commit()
        return id

    def add_new_shelf(self, letter):
        id = self.get_last_shelf_id(letter)
        id += 1
        self.curr.execute("INSERT INTO shelves VALUES (?,?)", (letter,id))
        self.conn.commit()
        return id
    def book_size(self,number_of_pages):
        return ((3 / 500) * number_of_pages + 0.5)

    def find_free_space(self, letter,shelf_id):
        sql_sum_pages = "SELECT SUM(pages) FROM (SELECT pages FROM book WHERE book_id in" \
                        "( SELECT book_id FROM books_on_shelves WHERE letter = '{}' and shelf_id = {}))".format(letter,shelf_id)
        self.curr.execute(sql_sum_pages)
        rows = self.curr.fetchall()
        number_of_pages = rows[0][0]
        if number_of_pages:
            space = shelf_size - self.book_size(number_of_pages)
        else:
            space = shelf_size
        return space
    def get_last_book_on_shelf(self,letter,shelf_id):
        sql_get_book = "SELECT * FROM  book  WHERE book_id in (SELECT book_id from (SELECT MAX( author_title), book_id" \
        "FROM  (SELECT(ahuthor + title) author_title, book_id  FROM books_on_shelves WHERE letter = {} and shelf_id = {})" \
        "GROUP BY book_id)) ".format(letter,shelf_id)
        self.curr.execute(sql_get_book)
        rows = self.curr.fetchall()
        return rows[0]

    def get_first_book_on_shelf(self, letter, shelf_id):
        sql_get_book = "SELECT * FROM  book  WHERE book_id in (SELECT book_id from (SELECT MIN( author_title), book_id" \
                       "FROM  (SELECT(ahuthor + title) author_title, book_id  FROM books_on_shelves WHERE letter = {} and shelf_id = {})" \
                       "GROUP BY book_id)) ".format(letter, shelf_id)
        self.curr.execute(sql_get_book)
        rows = self.curr.fetchall()
        return rows[0]
    def replace_book_on_shelf(self, book_id,letter, new_shelf_id):
        sql_replace_book ="UPDATE books_on_shelves SET  shelf_id={}  WHERE letter = {} AND book_id={}".format(new_shelf_id,letter,book_id)
        self.curr.execute(sql_replace_book)

    def sort_shelves(self,letter,shelf_id):
        if shelf_id <= 1:
            return
        temp = self.get_first_book_on_shelf(letter, shelf_id )
        first_id = temp[0]
        first_book = bk.Book(temp[1],temp[2],temp[3])
        temp = self.get_last_book_on_shelf(letter,(shelf_id -1))
        last_id = temp[0]
        last_book = bk.Book(temp[1],temp[2],temp[3])
        if last_book > first_book:
            self.replace_book_on_shelf(last_id,letter,shelf_id)
            self.replace_book_on_shelf(first_id, letter, (shelf_id -1))
            self.sort_shelves(letter,(shelf_id -1))

    def remove_book_from_shelf(self, book_id):
        self.curr.execute("DELETE FROM books_on_shelves WHERE book_id=?", (book_id,))

    def place_book_on_shelf(self, book_id):
        sql_get_book = "SELECT * FROM book WHERE book_id = {}".format(book_id)
        self.curr.execute(sql_get_book)
        rows = self.curr.fetchall()
        for book in rows:
            first_letter  =  book[2][0].upper()
            shelf_id = self.get_last_shelf_id(first_letter)
            number_of_pages = book[3]
            free_space = self.find_free_space(first_letter,shelf_id)  - self.book_size(number_of_pages)
            if free_space <= 0:
                shelf_id = self.add_new_shelf(first_letter)
            sql_place_book ="INSERT INTO books_on_shelves VALUES('{}',{},{})".format(first_letter,shelf_id,book_id)
            self.curr.execute(sql_place_book)
            self.conn.commit( )
            self.sort_shelves(first_letter,shelf_id)

    def view_books(self):
        self.curr.execute("SELECT * FROM book")
        rows = self.curr.fetchall()
        return rows
    def delete_by_title (self,title):
        self.curr.execute("DELETE FROM book WHERE title=?",(title,))
        self.conn.commit( )
    def search_book(self,title="",author=""):
        self.curr.execute("SELECT * FROM book WHERE title=? OR author=? ",(title,author))
        rows = self.curr.fetchall()
        return rows
    def delete(self,id):
        self.curr.execute("DELETE FROM book WHERE book_id=?",(id,))
        self.conn.commit()
    def update(self,id,title,author,book_id):
        self.curr.execute("UPDATE book SET  title=? AND author=?  WHERE  book_id=?",(book_id,title, author,))
        self.conn.commit( )
    def __del__(self):
        self.conn.close()
myLib = Init_Library("books3.db")