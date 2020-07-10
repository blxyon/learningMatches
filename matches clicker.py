import tkinter as tk
from tkinter import messagebox
import os.path
from datetime import datetime



#inspired by
#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#a very interesting answer here too:
#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter#:~:text=One%20way%20to%20switch%20frames,use%20any%20generic%20Frame%20class.
class MainApplication(tk.Frame):
    def __init__(self, parent, txt, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent#I guess this says that the parent of itself, the frame is the root, which is passed in the argument called parent
        self.txt = txt#same here
        parent.geometry("400x100+100+100")
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.incButton=tk.Button(text="Add a match played",command=lambda:self.add())
        self.incButton.pack()
        self.score=tk.Label(root)
        self.configureScore(txt.getLastScore())
        self.score.pack()
        self.label=tk.Label(root)
        self.pickWhatToDo()
        self.label.pack()
        self.decButton=tk.Button(text="Add a challenge done",command=lambda:self.dec())
        self.decButton.pack()
    def on_closing(self):
        #when closing it will show the warning box function and therefore end the txt file usage
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.txt.file_object.close()
            self.parent.destroy()
    def configureScore(self,intScore):
        #it helps the to always show a positive value in the GUI
        if((intScore)>=0):
            self.score.configure(text=str(intScore))
        else:
            self.score.configure(text=str(-(intScore)))

        
    def add(self):
        #button funct
        lastScore=self.txt.getLastScore()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")#string format
        line1="You have added a game at the time: "+dt_string+"\n"
        line2="Score="+str(lastScore+1)+"\n"
        self.txt.writeAndDisplay(line1)
        self.txt.writeAndDisplay(line2)
        self.configureScore(lastScore+1)
        self.pickWhatToDo()
        
    def dec(self):
        lastScore=self.txt.getLastScore()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line1="You have added a challenge at the time: "+dt_string+"\n"
        line2="Score="+str(lastScore-1)+"\n"
        self.txt.writeAndDisplay(line1)
        self.txt.writeAndDisplay(line2)
        self.configureScore(lastScore-1)
        self.pickWhatToDo()
    def pickWhatToDo(self):
        #fancy labels
        lastScore=self.txt.getLastScore()
        if(lastScore==0):
            s=("Great work, keep me balanced!")
        elif(lastScore>0):
            s=("Those are the number of challenges you got to be doing.")
        elif(lastScore<0):
            s=("Great work, you deserve to be playing a match of something! Keep it up!")
        self.label.configure(text=s)



#reminder: setting something self. will make an obejct accsessible anywhere in the class
#not making a variable self. will only make it local to the method that deals with it
class TextHandlerApp():
    def __init__(self):
        self.file_object=open("logGames.txt","a+")
        #getsize does count spaces!!!
        #some validation
        if not (os.path.exists("logGames.txt")):
            self.createATxt()
        else:
            fileSize=os.path.getsize("logGames.txt")
            if fileSize==0:
                self.createATxt()
        self.formatLog()
        self.readTheInitialTxt()
    def createATxt(self):
        #initialization of the txt
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.file_object.write("This file was initialized at the time: "+dt_string+"\n")
        self.file_object.write("Score="+"0"+"\n")
    def formatLog(self):
        #formats the cached list
        self.file_object.seek(0)
        wholeLog=self.file_object.read();
        self.formatedDoc=[]
        temp=""
        for char in wholeLog:
            if(char!="\n"):
                temp=temp+char
            else:
                self.formatedDoc.append(temp)
                temp=""
    def writeAndDisplay(self,line):
        #writes to the file, the list and to the terminal
        self.formatedDoc.append(line)
        self.file_object.write(line)
        #we ensure the format is the same everywhere(txt and console)
        #by taking a substring
        print(line[:(len(line)-1)])
    def getLastScore(self):
        #gets the last score from the cached list list
        lastLineNo=len(self.formatedDoc)-1
        for i in range(0,len(self.formatedDoc[lastLineNo])):
            if self.formatedDoc[lastLineNo][i]=="=":
                return int(self.formatedDoc[lastLineNo][(i+1):])
    def readTheInitialTxt(self):
        for line in self.formatedDoc:
            print (line)
    



    
if __name__ == "__main__":
    txt=TextHandlerApp()
    root = tk.Tk()
    MainApplication(root,txt).pack(side="top", fill="both", expand=True)
    root.mainloop()






#tkinter



    






root.mainloop()

