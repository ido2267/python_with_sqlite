# python_with_sqlite
The liberary project using sqlite advantages
Class Liberary:


Functions:
•	Constructor : receives database name. number of shelves allowed 
Connects to database
Create cursors for all tables. 
Open or creates tables of database
Commit changes

•	Print books for writer (gets a writer name and prints the books for that writer in every shelf)
•	Print library (prints all library in parallel threads)
•	Replace a book (receives  a new book and an old book's name. replace the old book that is on the shelf with the new book)

Tables:

Table books:
Columns:
Book's name
Writer's name
Number of pages
Id number

Table Shelf:
Columns:
Letter – only writer's that their name starts with that letter will be presented on this shelf
Shelf's size – the size of the shelf in centimeters
Shelf number. There can be more than one shelf for every letter

Table Shelves:
Columns:
Letter & number: The key of the shelf
Book's  Id: for each book on shelf there will be a row on shelves 
 

Table Reader:
Columns:
Reader's name   
Reader's Id
Number of books allowed



Table borrows:
Columns:
Reader's Id   
Book's Id 
Date taken

Program:
Write a program that presents to the user (with infinite loop):
1.	 Add a book (ask the user for book's details)
2.	Replace a book (receives the name of the returned book and the name of the 
Book that is given
3.	Print books for a writer (receives the writer's name)
4.	Print the entire liberaray
5.	Add a reader 

6.	Exit the program
