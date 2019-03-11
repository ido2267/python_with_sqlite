from tkinter import * 
import liberary as lb
import popup as pp
class showWindow:
    global selected_tuple
    
    def __init__(self):
        self.window = Tk()
        self.window.wm_title("Library")
        self.l1 = Label(self.window, text="Title")
        self.l1.grid(row=0, column=0)
        self.l2 = Label(self.window, text="Author")
        self.l2.grid(row=0, column=2)
        self.l3 = Label(self.window, text="Pages")
        self.l3.grid(row=1, column=0)
        self.l4 = Label(self.window, text="Shelf")
        self.l4.grid(row=1, column=2)

        self.title_text = StringVar()
        self.e1 = Entry(self.window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1)
        self.author_text = StringVar()
        self.e2 = Entry(self.window, textvariable=self.author_text)
        self.e2.grid(row=0, column=3)
        self.pages_text = StringVar()
        self.e3 = Entry(self.window, textvariable=self.pages_text)
        self.e3.grid(row=1, column=1)
        self.shelf_text = StringVar()
        self.e4 = Entry(self.window, textvariable=self.shelf_text)
        self.e4.grid(row=1, column=3)

        self.list1 = Listbox(self.window, height=6, width=55)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=3)
        sb1 = Scrollbar(self.window)
        sb1.grid(row=2, column=3, rowspan=6)
        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)
        self.list1.bind('<<ListboxSelect>>', self.get_selected_book)

        b1 = Button(self.window, text="View books", width=12, command=self.view_books)
        b1.grid(row=2, column=4)
        b2 = Button(self.window, text="Search book", width=12, command=self.search_book)
        b2.grid(row=3, column=4)
        b3 = Button(self.window, text="Add book", width=12, command=self.add_book)
        b3.grid(row=4, column=4)
        b4 = Button(self.window, text="Update selected", width=12, command=self.update_command)
        b4.grid(row=5, column=4)
        b5 = Button(self.window, text="Delete selected", width=12, command=self.delete_book)
        b5.grid(row=6, column=4)
        b5 = Button(self.window, text="Close", width=12, command=self.window.destroy)
        b5.grid(row=7, column=4)
# //////////////////////////////////////////////////////////////////

        self.l5 = Label(self.window, text="Reader")
        self.l5.grid(row=0, column=4)
        self.l6 = Label(self.window, text="Books allowed")
        self.l6.grid(row=1, column=4)

        self.list2 = Listbox(self.window, height=6, width=25)
        self.list2.grid(row=1, column=6, rowspan=6, columnspan=1)
        sb2 = Scrollbar(self.window)
        sb2.grid(row=2, column=7, rowspan=6)
        self.list2.configure(yscrollcommand=sb2.set)
        sb2.configure(command=self.list2.yview)
        self.list2.bind('<<ListboxSelect>>', self.get_selected_reader)

        self.reader_text = StringVar()
        self.e5 = Entry(self.window, textvariable=self.reader_text)
        self.e5.grid(row=0, column=5)
        self.readers_books_text = StringVar()
        self.e6 = Entry(self.window, textvariable=self.readers_books_text)
        self.e6.grid(row=1, column=5)

        b5 = Button(self.window, text="Add reader", width=12, command=self.new_reader_command)
        b5.grid(row=2, column=5)
        b5 = Button(self.window, text="Reader's list", width=12, command=self.view_readers)
        b5.grid(row=3, column=5)
        b6 = Button(self.window, text="Borrow book", width=12, command=self.borrow_book)
        b6.grid(row=4, column=5)
        b7 = Button(self.window, text="Return book", width=12, command=self.return_book)
        b7.grid(row=5, column=5)
        b7 = Button(self.window, text="Delete reader", width=12, command=self.delete_reader)
        b7.grid(row=6, column=5)
# ////////////////////////////////////////////////////////
        self.l7 = Label(self.window, text="Title")
        self.l7.grid(row=0, column=6)
        self.l8 = Label(self.window, text="Date taken")
        self.l8.grid(row=1, column=6)

        self.list3 = Listbox(self.window, height=6, width=35)
        self.list3.grid(row=1, column=8, rowspan=6, columnspan=1)
        self.list3.bind('<<ListboxSelect>>', self.books_for_reader)

        self.book_taken = StringVar()
        self.e7 = Entry(self.window, textvariable=self.book_taken)
        self.e7.grid(row=0, column=7)
        self.date_borrowed = StringVar()
        self.e8 = Entry(self.window, textvariable=self.date_borrowed)
        self.e8.grid(row=1, column=7)

        self.library = lb.Library("books3.db")
        self.window.mainloop()

    def get_selected_book(self,event):
        try:
            index=self.list1.curselection()[0]
            selected_tuple = self.list1.get(index)
            self.e1.delete(0,END)
            self.e1.insert(END,selected_tuple[0])
            self.e2.delete(0, END)
            self.e2.insert(END,selected_tuple[1])
            self.e3.delete(0,END)
            self.e3.insert(END,selected_tuple[2])
            self.e4.delete(0, END)
            self.e4.insert(END,selected_tuple[3])
        except:
            print("wrong line choice")

    def get_selected_reader(self, event):
        try:
            index = self.list2.curselection()[0]
            selected_tuple = self.list2.get(index)
            self.show_books_for_reader(selected_tuple[2])
            self.e5.delete(0, END)
            self.e5.insert(END, selected_tuple[0])
            self.e6.delete(0, END)
            self.e6.insert(END, selected_tuple[1])
        except:
            print("wrong line choice")

    def books_for_reader(self, event):
        try:
            index = self.list3.curselection()[0]
            selected_tuple = self.list3.get(index)
            self.e7.delete(0, END)
            self.e7.insert(END, selected_tuple[0])
            self.e8.delete(0, END)
            self.e8.insert(END, selected_tuple[1])
        except:
            print("wrong line choice")

    def view_books(self):
        self.list1.delete(0,END)
        for row in self.library.view_books():
            self.list1.insert(END,row)
    
    def search_book(self):
        self.list1.delete(0, END)
        for row in self.library.search_book(self.title_text.get(),self.author_text.get()):
            self.list1.insert(END, row)
            
    def new_reader_command(self):
        self.library.add_new_reader(self.reader_text.get(),self.readers_books_text.get())
        self.list2.delete(0, END)
        self.list2.insert(END,( self.reader_text.get(),self.readers_books_text.get()))
        self.view_readers()

    def view_readers(self):
        self.list2.delete(0, END)
        for row in  self.library.get_all_readers():
            self.list2.insert(END, row)
                              
    def add_book(self):
        self.list1.delete(0, END)
        id = self.library.add_new_book(self.title_text.get(), self.author_text.get(), self.pages_text.get())
        self.list1.insert(END,( self.title_text.get(),self.author_text.get(),self.pages_text.get(),self.shelf_text.get()))
    
    def delete_book(self):
        try:
            index = self.list1.curselection()[0]
            selected_tuple = self.list1.get(index)
            self.library.delete_book(selected_tuple[0])
            self.view_books()
            self.e1.delete(0,END)
            self.e2.delete(0,END)
            self.e3.delete(0,END)
            self.e4.delete(0,END)
        except Exception as error_message:
            alert_window = pp.popupWindow(error_message)

    def delete_reader(self):
        try:
            index = self.list2.curselection()[0]
            selected_tuple = self.list2.get(index)
            self.library.delete_reader(selected_tuple[2])
            self.view_readers()
            self.e5.delete(0, END)
            self.e6.delete(0, END)
            self.e7.delete(0, END)
            self.e8.delete(0, END)
        except Exception as error_message:
            alert_window = pp.popupWindow(error_message)
            
    def borrow_book(self):
        try:
            self.library.borrow_book(self.title_text.get(), self.author_text.get(),self.reader_text.get())
            reader_id = self.library.get_reader(self.reader_text.get())[0][2]
            self.show_books_for_reader(reader_id)

        except Exception as error_message:
            alert_window = pp.popupWindow(error_message)

    def return_book(self):
        try:
            self.library.return_book(self.book_taken.get())
            self.e7.delete(0, END)
            self.e8.delete(0, END)
            self.list3.delete(0,END)
            self.view_books()
        except Exception as error_message:
            alert_window = pp.popupWindow(error_message)

    def update_command(self):
        self.library.update( selected_tuple[0], self.title_text.get(), self.author_text.get(), self.pages_text.get(), self.shelf_text.get())
        self.view_books()

    def show_books_for_reader(self,reader_id):
        self.list3.delete(0, END)

        for row in self.library.show_readers_books(reader_id):
            self.list3.insert(END, row)

newWindow = showWindow()

    
    
