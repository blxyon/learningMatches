import tkinter as tk
from datetime import datetime
class ActivityUnitedSystem:
    def __init__(self,parent,*args,**kwargs):
        self.parent=parent

        self.lastScore=self.parent.txt.getLastScore("=")
        
        self.procastinationFr=UnproductiveFr(self)
        self.procastinationFr.grid(row=0,column=0,sticky="news")

        self.scoreFr=scoreFr(self)
        self.scoreFr.grid(row=1,column=0,sticky="news")
        
        self.messageFr=messageFr(self)
        self.messageFr.grid(row=2,column=0,sticky="news")
        
        self.productivityFr=ProductiveFr(self)
        self.productivityFr.grid(row=3,column=0,sticky="news")
    def addActivity(self,activity,addVal):
        #button function only
        now = datetime.now()
        self.lastScore=self.lastScore+addVal
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")#string format
        #4 spaces followed by "-" and the activity
        line1="    - "+activity+", at the time: "+dt_string+"| ("+str(addVal)+") S="+str(self.lastScore)+"\n"
        self.parent.txt.writeAndDisplay(line1)
        self.scoreFr.configureScore()
        self.messageFr.pickWhatToDo()
    
    
class ProductiveFr(tk.Frame,ActivityUnitedSystem):
    def __init__(self,system, *args,**kwargs):
        tk.Frame.__init__(self,system.parent,*args,**kwargs)
        self.challenges={"easy challenge":-2,"medium challenge":-4,"hard challenge":-6,"medium read":-1,"long read":-3}
        self.buttonList=[]
        i=0
        j=0
        counter=0
        for key, value in self.challenges.items():
            if(i==2):
                i=0
                j=j+1
            self.buttonList.append(tk.Button(self,text="Add: "+key+" done"+"("+str(value)+")",command=lambda k=key,v=value:system.addActivity(k,v)))
            self.buttonList[counter].grid(row=j,column=i)  
            i=i+1
            counter=counter+1

class UnproductiveFr(tk.Frame,ActivityUnitedSystem):
    def __init__(self, system, *args, **kwargs):
        tk.Frame.__init__(self,system.parent,*args,**kwargs)
        self.proc={"quick match":1,"medium match":3,"youtube unproductive video":2,"average procastination":4,"very long procastination":6}
        self.buttonList=[]
        i=0
        j=0
        counter=0
        for key, value in self.proc.items():
            if(i==2):
                i=0
                j=j+1
            self.buttonList.append(tk.Button(self,text="Add: "+key+" done"+"("+str(value)+")",command=lambda k=key,v=value:system.addActivity(k,v)))
            self.buttonList[counter].grid(row=j,column=i)  
            i=i+1
            counter=counter+1
        

class messageFr(tk.Frame):
    def __init__(self,system,*args,**kwargs):
        tk.Frame.__init__(self,system.parent,*args,**kwargs)
        self.system=system
        self.label=tk.Label(self)
        self.pickWhatToDo()
        self.label.pack()#only one message
    def pickWhatToDo(self):
        #fancy labels
        if(self.system.lastScore==0):
            s=("Great work, keep me balanced!")
        elif(self.system.lastScore>0):
            s=("Those are the number of challenges you got to be doing.")
        elif(self.system.lastScore<0):
            s=("Great work, you deserve to be playing a match of something! Keep it up!")
    
        self.label.configure(text=s)

class scoreFr(tk.Frame):
    def __init__(self,system,*args,**kwargs):
        tk.Frame.__init__(self,system.parent,*args,**kwargs)
        self.system=system
        self.score=tk.Label(self)
        self.configureScore()
        self.score.pack()#only one score
    def configureScore(self):
        #it helps the to always show a positive value in the GUI
        if((self.system.lastScore)>=0):
            self.score.configure(text=str(self.system.lastScore))
        else:
            self.score.configure(text=str(-(self.system.lastScore)))
