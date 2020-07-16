
import os
from datetime import datetime
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
        self.getRemainders()
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
    def getLastScore(self,sign):
        #gets the last score from the cached list list
        #we first find its line
        lineWithLastScore=0
        
        lastLineNo=len(self.formatedDoc)
        for j in range(0,lastLineNo):
            if self.formatedDoc[j][:5]=="Score":
                lineWithLastScore=j
        
        for i in range(0,len(self.formatedDoc[lineWithLastScore])):
            if self.formatedDoc[lineWithLastScore][i]==sign:
                return int(self.formatedDoc[lineWithLastScore][(i+1):])
    def readTheInitialTxt(self):
        for line in self.formatedDoc:
            print (line)
    def getActNameAndDate(self,line):
        counter=0
        #could have used regedex--maybe in the future I will be making this whole class regedex based
        #as it will be much easily readable and shorter
        #this is a bit dumb such that the user must only type one activity
        #if they put more than one "," the program will break
        #there is an easy fix for it, will fix later
        dt_string=""
        actName=""
        readingState=False
        for i in range(0,len(line)):
            if (line[i]==":" and counter==0):
                counter=counter+1
                readingState=True
                #we will next need to get the activity name
            elif(counter==1 and line[i]==":"):
                counter=counter+1
                readingState=True
            elif(counter==2 and readingState==True):
                dt_string=dt_string+line[i]
            elif(counter==1 and line[i]=="," and readingState==True):
                readingState=False
            elif(counter==1 and readingState==True):
                actName=actName+line[i]
        return((actName,dt_string,))
                
    def getRemainders(self):
        self.remainders=set()
        for line in self.formatedDoc:
            if line[:8]=="Reminder":
               self.remainders.add(self.getActNameAndDate(line)) 
                #date_time_obj = datetime.strptime(self.getLastScore(":"), '%d/%m/%y %H:%M:%S')
