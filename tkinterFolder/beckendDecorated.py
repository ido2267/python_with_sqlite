import sqlite3 as sq3
def myDecorator(inFunction):
    def wrapper(*args,**kwargs):
        conn = sq3.connect("books.db")
        curr = conn.cursor()
        curr.execute(inFunction(*args))
        if inFunction.__name__ in ['view','search']:
            rows = curr.fetchall()
            conn.close()
            return rows
        conn.commit()
        conn.close()
    return wrapper

@myDecorator
def connect():
    return "CREATE TABLE IF NOT EXISTS book(id INTEGRER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER) "

@myDecorator
def insert(inStr):
    title, author, year, isbn = inStr.split('-')
    outStr = "INSERT INTO book VALUES (NULL,'{}','{}',{},{})".format(title,author,year,isbn)
    return outStr

@myDecorator
def view():
    return ("SELECT * FROM book")


@myDecorator
def delete_by_title (title):
    outStr = "DELETE FROM book WHERE title='{}' ".format(title)
    return outStr

@myDecorator
def search(inStr):
   title, author, year, isbn = inStr.split('-')
   outStr = "SELECT * FROM book WHERE title='{}' OR author='{}' OR year={} OR isbn={}".format(title,author,year,isbn)
   return (outStr)

@myDecorator
def delete(id):
    return "DELETE FROM book WHERE id={}".format(id)

@myDecorator
def update(inStr):
    id,title, author, year, isbn = inStr.split('-')
    outStr = "UPDATE book SET  title='{}' AND author='{}' AND year={} AND isbn={} WHERE  id={}".format(title, author, year, isbn,id)
    return outStr

connect()  # function will be executed every time interface.py will be executed

# delete_by_title("Robinzon Kruzo")
# insert ("hitchhiker guide to the galaxy-Douglas Adams-1978-10122888")
# delete(None)
# delete_by_title('Crime and punishement')
# update("9-My family and other animals-Gerald Durrell-1966-2161000222")
print (search(" -Grim Brothers-0-0"))

# content = view()
# for member in content:
#      print(member)
