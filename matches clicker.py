import tkinter as tk
from tkinter import messagebox
import os.path
from datetime import datetime

#tempScore
root=tk.Tk()
root.geometry("400x100+100+100")
file_object  = open("logGames.txt", "a+")
def createATxt():
    now = datetime.now()
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file_object.write("This file was initialized on the date: "+dt_string+"\n")
    file_object.write("Score="+"0"+"\n")

    return file_object
def formatLog():
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
    lastLineNo=len(formatedDoc)-1
    for i in range(0,len(formatedDoc[lastLineNo])):
        if formatedDoc[lastLineNo][i]=="=":
            return int(formatedDoc[lastLineNo][(i+1):])
def configureScore(intScore):
    if((intScore)>=0):
        score.configure(text=str(intScore))
    else:
        score.configure(text=str(-(intScore)))
def add():
    lastScore=getLastScore()
    now = datetime.now()
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    line1="You have added a game at: "+dt_string+"\n"
    line2="Score="+str(lastScore+1)+"\n"
    print(line1)
    print(line2)
    formatedDoc.append(line1)
    formatedDoc.append(line2)
    file_object.write(line1)
    file_object.write(line2)
    configureScore(lastScore+1)
    pickWhatToDo()
    
def dec():
    lastScore=getLastScore()
    now = datetime.now()
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    line1="You have added a game at: "+dt_string+"\n"
    line2="Score="+str(lastScore-1)+"\n"
    print(line1)
    print(line2)
    formatedDoc.append(line1)
    formatedDoc.append(line2)
    file_object.write(line1)
    file_object.write(line2)
    configureScore(lastScore-1)
    pickWhatToDo()
def pickWhatToDo():
    lastScore=getLastScore()
    if(lastScore==0):
        s=("Great work keep me balanced!")
    elif(lastScore>0):
        s=("Those are the challenges you got to be doing.")
    elif(lastScore<0):
        s=("Great work, you deserve to be playing a match of something! Keep it up!")
    label.configure(text=s)
    
#getsize does count spaces!!!
if not (os.path.exists("logGames.txt")):
    file_object  = createATxt()
else:
    fileSize=os.path.getsize("logGames.txt")
    if fileSize==0:
        file_object=createATxt()



formatedDoc=formatLog()

for line in formatedDoc:
    print (line)



incButton=tk.Button(text="Add matches played",command=lambda:add())
incButton.pack()

score=tk.Label(root)
configureScore(getLastScore())
score.pack()
label=tk.Label(root)
pickWhatToDo()
label.pack()
decButton=tk.Button(text="Add challenges done",command=lambda:dec())
decButton.pack()


    


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        file_object.close()
        root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

