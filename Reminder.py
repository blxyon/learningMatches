from datetime import datetime
from datetime import timedelta 
import tkinter as tk


def getCurrentTimeToList():
    now = datetime.now()
    dt_string = now.strftime("%d")
    dt_string2 = now.strftime("%m")
    dt_string3 = now.strftime("%Y")
    return ([dt_string,dt_string2,dt_string3])
class ReminderFr(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent=parent

        self.rowLabels=[]
        self.removeButtons=[]
        self.removedRows=[]
        self.sessionAddedRem=[]
        
        curYear=getCurrentTimeToList()[2]
        monthOptions = ["Month","1","2","3","4","5","6","7","8","9","10","11","12"]
        yearOptions =[curYear,str(int(curYear)+1),str(int(curYear)+2),str(int(curYear)+3),str(int(curYear)+4)]
        dayOptions=["Select Month"]

        self.addRemainderButton=tk.Button(self,text="Add remainder",command=lambda:self.add_remainder(butType="gen"))
        self.addRemainderButton.grid(row=2,column=0)

        self.addRem1wEEK=tk.Button(self,text="Add remainder for a week from now",command=lambda:self.add_remainder(butType="1week"))
        self.addRem1wEEK.grid(row=3,column=0)
        
        self.remainderVar = tk.StringVar()
        self.addTextBox=tk.Entry(self,textvariable=self.remainderVar)
        self.addTextBox.grid(row=1,column=0)
        
        self.remainderMonth=tk.StringVar()
        self.remainderMonth.trace("w",self.dateCallBack)#http://effbot.org/tkinterbook/variable.htm
        self.remainderMonth.set(monthOptions[0])
        self.monthOption=tk.OptionMenu(self,self.remainderMonth, *monthOptions)
        self.monthOption.grid(row=0,column=0,sticky="w")
        
        self.remainderYear=tk.StringVar()
        self.remainderYear.trace("w",self.dateCallBack)
        self.remainderYear.set(yearOptions[0])
        self.yearOption=tk.OptionMenu(self,self.remainderYear, *yearOptions)
        self.yearOption.grid(row=0,column=1,sticky="w")
        
        self.remainderDay=tk.StringVar()
        self.remainderDay.set(dayOptions[0])
        self.dayOption=tk.OptionMenu(self,self.remainderDay, *dayOptions)
        self.dayOption.grid(row=0,column=2,sticky="w")

        self.initialize_remainders()
    def add_remainder(self,butType):
        month=self.remainderMonth.get()
        
        now = datetime.now()
        dt_string2 = now.strftime("%d/%m/%Y %H:%M:%S")
        #
        
        reminderStr=self.remainderVar.get()
        if(reminderStr==""):
            reminderStr="_not_specified"

        if(month!="Month" and butType=="gen"):
            year=self.remainderYear.get()
            day=self.remainderDay.get()
            
            dt_string = ("%s/%s/%s"%(day,month,year,))#string format
            
            self.add_reminder(reminderStr,dt_string,dt_string2)
        elif(butType=="1week"):
            newDate=now+timedelta(days=7)
            dt_string=newDate.strftime("%d/%m/%Y")
            self.add_reminder(reminderStr,dt_string,dt_string2)
            
    def add_reminder(self,reminderStr,dt_string,dt_string2):
        now = datetime.now()
        todaysDateString=("%s/%s/%s"%(getCurrentTimeToList()[0],getCurrentTimeToList()[1],getCurrentTimeToList()[2],))
        appendDB=self.parent.db.add_reminder_to_table(reminderStr,dt_string,todaysDateString)
        todaysDate=now.date()
        #we must update the gui.. if necessary
        dateRemainder = datetime.strptime(dt_string,"%d/%m/%Y").date()
        if(todaysDate<=dateRemainder and appendDB==True):
                
            line1="    * "+reminderStr+", added for the time:"+dt_string+", at:"+dt_string2+"\n"
            self.parent.txt.writeAndDisplay(line1)
            self.sessionAddedRem.append((reminderStr,dt_string))
            self.removeAllRem()
            self.initialize_remainders()   
    def initialize_remainders(self):
        self.lastRemainderOnRow=0
        self.rowLabels=[]
        self.removeButtons=[]
        #print(self.parent.db.rem)
        if str(type(self.parent.db.rem))!="<class 'NoneType'>":
            todaysTime=datetime.now()
            todaysDate=todaysTime.date()
            for label in self.parent.db.rem:
                dateRemainder = datetime.strptime(label[1],"%d/%m/%Y").date()         
                if(todaysDate<=dateRemainder):
                    if label in self.sessionAddedRem:
                        l=tk.Label(self,text="*Reminder: "+label[0]+", on the date: "+label[1])
                    else:
                        l=tk.Label(self,text="Reminder: "+label[0]+", on the date: "+label[1])
                    l.grid(row=self.lastRemainderOnRow,column=3)
                    self.rowLabels.append(l)
                    
                    b=tk.Button(self,text="Remove",command=lambda index=self.lastRemainderOnRow,remStr=label[0], dd=label[1]:self.deleteReminder(index,remStr,dd))
                    self.removeButtons.append(b)
                    self.removeButtons[len(self.removeButtons)-1].grid(row=self.lastRemainderOnRow,column=4)
                
                    self.lastRemainderOnRow=self.lastRemainderOnRow+1
    def deleteReminder(self,index,desc,due_date):
        self.parent.db.remove_reminder(desc,due_date)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line1="    x "+desc+", added for the time:"+due_date+", removed at:"+dt_string+"\n"
        self.parent.txt.writeAndDisplay(line1)
        
        self.removeAllRem()
        self.initialize_remainders()
    def removeAllRem(self):
        for i in range(0,len(self.rowLabels)):
            self.rowLabels[i].destroy()
            self.removeButtons[i].destroy()
            
            
    def dateCallBack(self,*args):
        dayOptions=[]
        if(self.remainderMonth.get()!="Month"):
            self.remainderDay.set("1")#to always reset and get rid of later errors
            dayOptions.append("1")
            if int(self.remainderYear.get()) % 400 == 0:
                leapYear=True
                ifFeb=29
            elif int(self.remainderYear.get()) % 100 == 0:
                leapYear=False
                ifFeb=28
            elif int(self.remainderYear.get()) % 4 == 0:
                leapYear=True
                ifFeb=29
            else:
                leapYear=False
                ifFeb=28
            if(self.remainderMonth.get()=="2"):
                #set the day+1
                for i in range(2,ifFeb+1):
                    dayOptions.append(str(i))
            else:
                if ((int(self.remainderMonth.get())%2==0 and int(self.remainderMonth.get())<=6) or (int(self.remainderMonth.get())%2==1 and int(self.remainderMonth.get())>=9)):
                    for i in range(2,30+1):
                        dayOptions.append(str(i))
                elif ((int(self.remainderMonth.get())%2==1 and int(self.remainderMonth.get())<=7) or (int(self.remainderMonth.get())%2==0 and int(self.remainderMonth.get())>7)):
                    for i in range(2,31+1):
                        dayOptions.append(str(i))
            menu = self.dayOption["menu"]
            menu.delete(0, 'end')
            
            for string in dayOptions:
                menu.add_command(label=string, 
                                 command=lambda value=string: self.remainderDay.set(value))

                    
