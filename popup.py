from tkinter import * 

class popupWindow:

    def __init__(self,message):
        self.window = Tk()
        self.window.wm_title("Alert")
        self.l1 = Label(self.window, text=message)
        self.l1.grid(row=0, column=0)

        b1 = Button(self.window, text="Close", width=12, command=self.window.destroy)
        b1.grid(row=1, column=0)
        self.window.mainloop()



    
#popup =   popupWindow("hello")
