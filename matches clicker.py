import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sys
sys.dont_write_bytecode = True#really annoying python cache!

import activities as act
import Reminder as rem
import textHandler as txtHan
import activities as act
import dbHandler as dbH

#inspired by
#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#a very interesting answer here too:
#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter#:~:text=One%20way%20to%20switch%20frames,use%20any%20generic%20Frame%20class.
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #here we write the opening line in our txt
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent#this sets its parent to the one passed, which in our case is the root
        self.txt = txtHan.TextHandlerApp()
        self.db = dbH.DatabaseApp()
        
        #parent.geometry("450x200+100+100") #-this is a bit redundant since the window autoresizes to its content by default
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid_rowconfigure(4,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.activities=act.ActivityUnitedSystem(self)
        
        self.remindersFrame=rem.ReminderFr(self)
        self.remindersFrame.grid(row=4,column=0,sticky="news")

        self.txt.writeAndDisplay("Program started at:"+dt_string+"\n")
        
        #obviously untill I will come with a smarter looking gui this won't be a problem anymore:...
        #i must come up with a way to keep updating the remainder list too when I submit a remainder
        
    def on_closing(self):
        #when closing it will show the warning box function and therefore end the txt file usage
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            self.txt.writeAndDisplay("Score="+str(self.activities.lastScore)+"\n")
            self.txt.writeAndDisplay("Program ended at:"+dt_string+"\n\n")
            self.txt.file_object.close()
            self.db.closedb()
            self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app=MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()



