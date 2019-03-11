import sqlite3 as sq3
import book as bk

shelf_size = 50
days_to_borrow = 21
file_name = "bookdatabase.txt"
class Library():
    def __init__(self,db):
        _shelves_allwoed = 1000

        self.conn=sq3.connect(db)
        self.curr = self.conn.cursor()
        books_sql = "CREATE TABLE IF NOT EXISTS book(book_id INTEGRER PRIMARY KEY, title TEXT NOT NULL," \
                    " author TEXT NOT NULL, pages INTEGER NOT NULL) "
        self.curr.execute(books_sql)
        shelves_sql = "CREATE TABLE IF NOT EXISTS shelves(letter CHAR (1) NOT NULL, shelf_id INTEGER NOT NULL," \
                      " UNIQUE(letter, shelf_id) ON CONFLICT REPLACE) "
        self.curr.execute(shelves_sql)
        books_on_shelves = "CREATE TABLE IF NOT EXISTS books_on_shelves(letter CHAR (1) NOT NULL, shelf_id INTEGER NOT NULL ," \
                           "book_id INTEGRER  REFERENCES book(book_id) ," \
                           "FOREIGN KEY(letter,shelf_id) REFERENCES shelves(letter,shelf_id )) "
        self.curr.execute(books_on_shelves)
        reader_sql = "CREATE TABLE IF NOT EXISTS readers(name TEXT NOT NULL, books_allowed INTEGER NOT NULL," \
                     " reader_id INTEGER) "
        self.curr.execute(reader_sql)

        books_for_readers = "CREATE TABLE IF NOT EXISTS books_for_readers(reader_id INTEGRER NOT NULL REFERENCES readers(reader_id)," \
                            " book_id INTEGRER NOT NULL REFERENCES book(book_id), date_borrowed TEXT)"

        self.curr.execute(books_for_readers)
        self.conn.commit( )

    def get_last_id(self, sql_str):
        self.curr.execute(sql_str)
        rows = self.curr.fetchall()
        if rows[0][0]:
            id = int(rows[0][0])
        else:
            id = 0
        return id

    def get_last_book_id(self):
        sql_str ="SELECT MAX( book_id) FROM book "
        return self.get_last_id(sql_str)

    def get_last_reader_id(self):
        sql_str ="SELECT  MAX(reader_id ) FROM readers "
        return self.get_last_id(sql_str)

    def get_last_shelf_id(self,letter):
        sql_str = "SELECT MAX( shelf_id) FROM shelves WHERE letter = '{}' ".format(letter)
        return self.get_last_id(sql_str)

    def add_new_book(self,title,author,pages):
        book_id = self.get_last_book_id()
        book_id +=1
        sql_add_book = "INSERT INTO book (book_id,title, author,pages) VALUES (?, ?,?,?)"
        self.curr.execute(sql_add_book, (book_id,title,author,pages))
        self.conn.commit( )
        self.place_book_on_shelf(book_id)
        return book_id

    def add_new_reader(self, name, books_allowed=2):
        id = self.get_last_reader_id()
        id += 1
        self.curr.execute("INSERT INTO readers VALUES (?,?,?)", (name, books_allowed, id))
        self.conn.commit()
        return id
    def get_all_readers(self):
        sql_readers = "SELECT * FROM readers"
        self.curr.execute(sql_readers)
        rows = self.curr.fetchall()
        return rows
    def get_reader(self, reader_name):
        sql_readers = "SELECT * FROM readers WHERE name = '{}' ".format(reader_name)
        self.curr.execute(sql_readers )
        rows = self.curr.fetchall()
        return rows
    def add_new_shelf(self, letter):
        id = self.get_last_shelf_id(letter)
        id += 1
        sql_shelf = "INSERT INTO shelves( letter, shelf_id)  VALUES  ('{}',{})".format(letter,id)
        self.curr.execute(sql_shelf )
        self.conn.commit()
        return id
    def book_size(self,number_of_pages):
        return ((3 / 500) * number_of_pages + 0.5)

    def find_free_space(self, letter,shelf_id):
        sql_sum_pages = "SELECT SUM(pages) FROM (SELECT pages FROM book WHERE book_id in " \
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
        "FROM  (SELECT(ahuthor + title) author_title, book_id  FROM books_on_shelves WHERE letter = '{}' and shelf_id = {})" \
        "GROUP BY book_id)) ".format(letter,shelf_id)
        self.curr.execute(sql_get_book)
        rows = self.curr.fetchall()
        return rows[0]

    def get_first_book_on_shelf(self, letter, shelf_id):
        sql_get_book = "SELECT * FROM  book  WHERE book_id in (SELECT book_id from (SELECT MIN( author_title), book_id" \
                       "FROM  (SELECT(ahuthor + title) author_title, book_id  FROM books_on_shelves WHERE letter = '{}' and shelf_id = {})" \
                       "GROUP BY book_id)) ".format(letter, shelf_id)
        self.curr.execute(sql_get_book)
        rows = self.curr.fetchall()
        return rows[0]
    def replace_book_on_shelf(self, book_id,letter, new_shelf_id):
        sql_replace_book ="UPDATE books_on_shelves SET  shelf_id={}  WHERE letter = '{}' AND book_id={}".format(new_shelf_id,letter,book_id)
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
        self.conn.commit()

    def place_book_on_shelf(self, book_id):
        sql_get_book = "SELECT * FROM book WHERE book_id = {}".format(book_id)
        self.curr.execute(sql_get_book)
        rows = self.curr.fetchall()
        first_letter  = rows[0][2][0]
        shelf_id = self.get_last_shelf_id(first_letter)
        if shelf_id == 0 :
            shelf_id = self.add_new_shelf(first_letter)
        number_of_pages = rows[0][3]
        free_space = self.find_free_space(first_letter,shelf_id)  - self.book_size(number_of_pages)
        if free_space <= 0:
            shelf_id = self.add_new_shelf(first_letter)
        sql_place_book ="INSERT INTO books_on_shelves VALUES('{}',{},{})".format(first_letter,shelf_id,book_id)
        self.curr.execute(sql_place_book)
        self.conn.commit( )
        self.sort_shelves(first_letter,shelf_id)
    def view_books(self):
        self.curr.execute("SELECT  bk.title, bk.author, bk.pages, (bks.letter ||  bks.shelf_id) as shelid "
                          " FROM book bk, books_on_shelves bks WHERE bk.book_id = bks.book_id ")
        rows = self.curr.fetchall()
        return rows

    def search_book(self,title="",author=""):
        sql_search = "SELECT bk.title, bk.author, bk.pages, bks.letter_shelf FROM" \
                     " (SELECT title,author, pages , book_id FROM book  WHERE title ='{}' OR author ='{}' )bk " \
                     "LEFT JOIN (SELECT (letter || shelf_id) AS letter_shelf , book_id FROM books_on_shelves) bks " \
                     "ON bk.book_id = bks.book_id".format(title,author)
        self.curr.execute( sql_search)
        rows = self.curr.fetchall()
        return rows

    def delete_reader(self, reader_id):
        self.curr.execute("SELECT COUNT(*) from books_for_readers WHERE reader_id=?", (reader_id,))
        rows = self.curr.fetchall()
        count = rows[0][0]
        if count > 0:
            raise ValueError("You can not delete a reader before returning all his books")
        else:
            self.curr.execute("DELETE FROM readers WHERE reader_id=?", (reader_id,))
    def delete_book(self, title):
        try:
            self.curr.execute("SELECT book_id FROM book WHERE title=?", (title,))
            rows = self.curr.fetchall()
            book_id = rows[0]
            count = self.curr.execute("SELECT COUNT(*) from books_for_readers WHERE book_id=?",(book_id,))
            if count > 0 :
                raise ValueError("Book can not be deleted while borrowed")
            self.curr.execute("DELETE FROM book WHERE book_id=?",(book_id,))
            self.remove_book_from_shelf(book_id)
            self.conn.commit()
        except Exception as e:
            print (e)
            raise
    def update(self,id,title,author,book_id):
        self.curr.execute("UPDATE book SET  title=? AND author=?  WHERE  book_id=?",(book_id,title, author,))
        self.conn.commit( )
    def get_book_id(self,book_title ):
        self.curr.execute("SELECT book_id FROM book WHERE title=? ", (book_title ,))
        rows = self.curr.fetchall()
        return rows
    def check_reader(self,reader_id,books_allwoed):
        self.curr.execute("SELECT  julianday(date('now')) - julianday(date_borrowed) FROM books_for_readers WHERE reader_id =?", (format(reader_id,)))
        rows = self.curr.fetchall()
        if len(rows) >= books_allwoed:
           print("Reader allready have {} books".format(books_allwoed))
           return False
        for row in rows:
            if row[0] >=  days_to_borrow:
                print("Reader should return a book")
                return False
        return True
    def give_book_to_reader(self,reader_id,books_allwoed,book_id):
        if self.check_reader(reader_id,books_allwoed):
            sql_borrow = "INSERT INTO books_for_readers  (reader_id,book_id,date_borrowed) VALUES({},{},date('now'))".format(reader_id,book_id)
            self.curr.execute(sql_borrow)
            self.conn.commit()
        else:
            raise ValueError ("Reader is not allowed to borrow more books")

    def borrow_book(self,book_title,book_author, reader_name):
        try:
            reader_detail = self.get_reader(reader_name)
            reader_id = reader_detail [0][2]
            books_allwoed = reader_detail[0][1]
            book_id = self.get_book_id(book_title)[0][0]
            self.give_book_to_reader (reader_id,books_allwoed,book_id)
            self.remove_book_from_shelf(book_id)
        except Exception as error_message:
            print(error_message)
            raise
    def take_book_from_reader(self,book_id ):
        sql_return_book ="DELETE FROM books_for_readers WHERE book_id =?"
        self.curr.execute(sql_return_book,(book_id,))
        self.conn.commit()
    def return_book(self, book_title):
        try:
            book_id = self.get_book_id(book_title )[0][0]
            self.place_book_on_shelf( book_id)
            self.take_book_from_reader(book_id)
        except Exception as error_message:
            print(error_message)
            raise

    def show_readers_books(self,reader_id):
        sql_borrow = "SELECT bk.title, bfr.date_borrowed FROM  books_for_readers bfr, book bk  WHERE reader_id = {}" \
                     " AND bk.book_id = bfr.book_id ".format(reader_id)
        self.curr.execute(sql_borrow)
        return self.curr.fetchall()
    def __del__(self):
        self.conn.close()
