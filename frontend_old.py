from tkinter import * 
import liberary as lb

class showWindow:
    global selected_tuple
    
    def __init__(self):
        self.window = Tk()
        self.window.wm_title("Library")
        self.l1 = Label(self.window, text="Title")
        self.l1.grid(row=0, column=0)
        self.l2 = Label(self.window, text="Author")
        self.l2.grid(row=0, column=2)
        self.l3 = Label(self.window, text="pages")
        self.l3.grid(row=1, column=0)
        self.l4 = Label(self.window, text="shelf")
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
        self.list1 = Listbox(self.window, height=6, width=35)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=2)
        sb1 = Scrollbar(self.window)
        sb1.grid(row=2, column=2, rowspan=6)
        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)
        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)
        b1 = Button(self.window, text="View all", width=12, command=self.view_command)
        b1.grid(row=2, column=3)
        b2 = Button(self.window, text="Search book", width=12, command=self.search_command)
        b2.grid(row=3, column=3)
        b3 = Button(self.window, text="Add book", width=12, command=self.add_command)
        b3.grid(row=4, column=3)
        b4 = Button(self.window, text="Update selected", width=12, command=self.update_command)
        b4.grid(row=5, column=3)
        b5 = Button(self.window, text="Delete selected", width=12, command=self.delete_command)
        b5.grid(row=6, column=3)
        b5 = Button(self.window, text="Close", width=12, command=self.window.destroy)
        b5.grid(row=7, column=3)
        self.library = lb.Library("books.db")
        self.window.mainloop()

    def get_selected_row(self,event):
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
            #print (selected_tuple) #debug
        except:
            print ("wrong choise of line")
    
    def view_command(self):
        self.list1.delete(0,END)
        for row in self.library.view_books():
            self.list1.insert(END,row)
    
    def search_command(self):
        self.list1.delete(0, END)
        for row in self.library.search_book(self.title_text.get(),self.author_text.get()):
            self.list1.insert(END, row)
    
    def add_command(self):
        self.list1.delete(0, END)
        id = self.library.add_new_book(self.title_text.get(), self.author_text.get(), self.pages_text.get())
        self.list1.insert(END,( self.title_text.get(),self.author_text.get(),self.pages_text.get(),self.shelf_text.get()))
    
    def delete_command(self):
        index = self.list1.curselection()[0]
        selected_tuple = self.list1.get(index)
        self.library.delete(selected_tuple[0])
        self.view_command()
        self.e1.delete(0,END)
        self.e2.delete(0,END)
        self.e3.delete(0,END)
        self.e4.delete(0,END)

    def update_command(self):
        self.library.update( selected_tuple[0], self.title_text.get(), self.author_text.get(), self.pages_text.get(), self.shelf_text.get())
        self.view_command()

newWindow = showWindow()

    
    
