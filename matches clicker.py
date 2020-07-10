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
        parent.geometry("450x200+100+100")
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid_rowconfigure(3,weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        self.procastinationFr=tk.Frame(self,background="blue")
        self.procastinationFr.grid(row=0,column=0,sticky="news")

        self.scoreFr=tk.Frame(self)
        self.scoreFr.grid(row=1,column=0,sticky="news")
        
        self.messageFr=tk.Frame(self)
        self.messageFr.grid(row=2,column=0,sticky="news")
        
        self.prodcutivityFr=tk.Frame(self,background="blue")
        self.prodcutivityFr.grid(row=3,column=0,sticky="news")


        
        self.incButton=tk.Button(self.procastinationFr,text="Add a quick match played(+1)",command=lambda:self.add(1))
        self.incButton.grid(row=0,column=0)
        self.incButton2=tk.Button(self.procastinationFr,text="Add a medium match played(+3)",command=lambda:self.add(3))
        self.incButton2.grid(row=0,column=1)
        self.incButton3=tk.Button(self.procastinationFr,text="Add a youtube unproductive video played(+2)",command=lambda:self.add(2))
        self.incButton3.grid(row=1,column=0)
        self.incButton4=tk.Button(self.procastinationFr,text="Add an average procastination(+4)",command=lambda:self.add(4))
        self.incButton4.grid(row=1,column=1)
        self.incButton5=tk.Button(self.procastinationFr,text="Add a very long procastination(+6)",command=lambda:self.add(6))
        self.incButton5.grid(row=2,column=0)
        
        self.score=tk.Label(self.scoreFr)
        self.configureScore(txt.getLastScore())
        self.score.pack()#only one score
        self.label=tk.Label(self.messageFr)
        self.pickWhatToDo()
        self.label.pack()#only one message
        
        self.decButton=tk.Button(self.prodcutivityFr,text="Add an easy challenge done(-2)",command=lambda:self.dec(2))
        self.decButton.grid(row=0,column=0)
        self.dec2Button=tk.Button(self.prodcutivityFr,text="Add a medium challenge done(-4)",command=lambda:self.dec(4))
        self.dec2Button.grid(row=0,column=1)
        self.dec3Button=tk.Button(self.prodcutivityFr,text="Add an hard challenge done(-6)",command=lambda:self.dec(6))
        self.dec3Button.grid(row=1,column=0)
        self.dec4Button=tk.Button(self.prodcutivityFr,text="Add a medium read about a subject(-1)",command=lambda:self.dec(1))
        self.dec4Button.grid(row=1,column=1)
        self.dec5Button=tk.Button(self.prodcutivityFr,text="Add a long read about a subject(-3)",command=lambda:self.dec(3))
        self.dec5Button.grid(row=2,column=0)
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

        
    def add(self,addVal):
        #button funct
        lastScore=self.txt.getLastScore()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")#string format
        line1="You have added a game at the time: "+dt_string+"|-(+"+str(addVal)+")"+"\n"
        line2="Score="+str(lastScore+addVal)+"\n"
        self.txt.writeAndDisplay(line1)
        self.txt.writeAndDisplay(line2)
        self.configureScore(lastScore+addVal)
        self.pickWhatToDo()
        
    def dec(self,decVal):
        lastScore=self.txt.getLastScore()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line1="You have added a challenge at the time: "+dt_string+"|-(-"+str(decVal)+")"+"\n"
        line2="Score="+str(lastScore-decVal)+"\n"
        self.txt.writeAndDisplay(line1)
        self.txt.writeAndDisplay(line2)
        self.configureScore(lastScore-decVal)
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
    app=MainApplication(root,txt)
    app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()



