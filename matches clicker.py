import tkinter as tk
from tkinter import messagebox
import os.path
from datetime import datetime


root=tk.Tk()
root.geometry("400x100+100+100")
file_object  = open("logGames.txt", "a+")
def createATxt():
    #initialization of the txt
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file_object.write("This file was initialized at the time: "+dt_string+"\n")
    file_object.write("Score="+"0"+"\n")

    return file_object
def formatLog():
    #formats the cached list
    file_object.seek(0)
    wholeLog=file_object.read();
    formatedDoc=[]
    temp=""
    for char in wholeLog:
        if(char!="\n"):
            temp=temp+char
        else:
            formatedDoc.append(temp)
            temp=""
    return formatedDoc
def getLastScore():
    #gets the last score from the cached list list
    lastLineNo=len(formatedDoc)-1
    for i in range(0,len(formatedDoc[lastLineNo])):
        if formatedDoc[lastLineNo][i]=="=":
            return int(formatedDoc[lastLineNo][(i+1):])
def configureScore(intScore):
    #it helps the to always show a positive value in the GUI
    if((intScore)>=0):
        score.configure(text=str(intScore))
    else:
        score.configure(text=str(-(intScore)))
def writeAndDisplay(line):
    #writes to the file, the list and to the terminal
    formatedDoc.append(line)
    file_object.write(line)
    #we ensure the format is the same everywhere(txt and console)
    #by taking a substring
    print(line[:(len(line)-1)])
    
def add():
    #button funct
    lastScore=getLastScore()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")#string format
    line1="You have added a game at the time: "+dt_string+"\n"
    line2="Score="+str(lastScore+1)+"\n"
    writeAndDisplay(line1)
    writeAndDisplay(line2)
    configureScore(lastScore+1)
    pickWhatToDo()
    
def dec():
    lastScore=getLastScore()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    line1="You have added a challenge at the time: "+dt_string+"\n"
    line2="Score="+str(lastScore-1)+"\n"
    writeAndDisplay(line1)
    writeAndDisplay(line2)
    configureScore(lastScore-1)
    pickWhatToDo()
def pickWhatToDo():
    #fancy labels
    lastScore=getLastScore()
    if(lastScore==0):
        s=("Great work, keep me balanced!")
    elif(lastScore>0):
        s=("Those are the number of challenges you got to be doing.")
    elif(lastScore<0):
        s=("Great work, you deserve to be playing a match of something! Keep it up!")
    label.configure(text=s)
    
#getsize does count spaces!!!
#some validation
if not (os.path.exists("logGames.txt")):
    file_object  = createATxt()
else:
    fileSize=os.path.getsize("logGames.txt")
    if fileSize==0:
        file_object=createATxt()



formatedDoc=formatLog()
for line in formatedDoc:
    print (line)


#tkinter
incButton=tk.Button(text="Add a match played",command=lambda:add())
incButton.pack()
score=tk.Label(root)
configureScore(getLastScore())
score.pack()
label=tk.Label(root)
pickWhatToDo()
label.pack()
decButton=tk.Button(text="Add a challenge done",command=lambda:dec())
decButton.pack()


    


def on_closing():
    #when closing it will show the warning box function and therefore end the txt file usage
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        file_object.close()
        root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()

