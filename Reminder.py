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
        repDaysList=["Repetition time"]+list(range(1,101))
        monthOptions = ["Month","1","2","3","4","5","6","7","8","9","10","11","12"]
        yearOptions =[curYear,str(int(curYear)+1),str(int(curYear)+2),str(int(curYear)+3),str(int(curYear)+4)]
        dayOptions=["Select Month"]

        self.addRemainderButton=tk.Button(self,text="Add reminder",command=lambda:self.add_reminder("gen"))
        self.addRemainderButton.grid(row=2,column=0)

        self.addRem1wEEK=tk.Button(self,text="Add reminder for a week from now",command=lambda:self.add_reminder("1week"))
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

        self.repDays=tk.StringVar()
        self.repDays.set(repDaysList[0])
        self.repDaysOption=tk.OptionMenu(self,self.repDays,*repDaysList)
        self.repDaysOption.grid(row=2,column=1)

        self.initialize_remainders()
    def add_reminder(self,*args):
        #inspired by : https://stackoverflow.com/questions/5079609/methods-with-the-same-name-in-one-class-in-python
        if len(args)==1 and isinstance(args[0],str):
            butType=args[0]
            month=self.remainderMonth.get()
            
            now = datetime.now()
            nowDateStrHour = now.strftime("%d/%m/%Y %H:%M:%S")
            
            reminderStr=self.remainderVar.get()
            if(reminderStr==""):
                reminderStr="_not_specified"
                
            repetition=self.repDays.get()
                
            if(repetition=="Repetition time"):
                repetition="None"
                
            if(month!="Month" and butType=="gen"):
                year=self.remainderYear.get()
                day=self.remainderDay.get()
                
                
                dateReminder = ("%s/%s/%s"%(day,month,year,))#string format
                
                self.add_reminder(reminderStr,dateReminder,nowDateStrHour,repetition)
            elif(butType=="1week"):
                newDate=now+timedelta(days=7)
                newDateStr=newDate.strftime("%d/%m/%Y")
                self.add_reminder(reminderStr,newDateStr,nowDateStrHour,repetition)
        elif len(args)==4:
            reminderStr=args[0]
            dateReminderStr=args[1]
            nowDateStrHour=args[2]
            repetition=args[3]
            
            now = datetime.now()
            todaysDateString=now.strftime("%d/%m/%Y")#("%s/%s/%s"%(getCurrentTimeToList()[0],getCurrentTimeToList()[1],getCurrentTimeToList()[2],))
            appendDB=self.parent.db.add_reminder_to_table(reminderStr,dateReminderStr,todaysDateString,repetition)
            todaysDate=now.date()
            #we must update the gui.. if necessary
            dateRemainder = datetime.strptime(dateReminderStr,"%d/%m/%Y").date()
            dateRemainder = self.calculateCurrentRep(repetition,dateRemainder,todaysDate)
            if(todaysDate<=dateRemainder and appendDB==True):
                line1="    * "+reminderStr+", added for the time:"+dateReminderStr+", at:"+nowDateStrHour+", repeats every: "+repetition+" days"+"\n"
                self.parent.txt.writeAndDisplay(line1)
                self.sessionAddedRem.append((reminderStr,dateReminderStr,todaysDateString,repetition))
                self.removeAllRem()
                self.initialize_remainders()
            
    
    def checkColourToUse(self,todaysDate,dateRemainder):
        colour="white"
        if todaysDate==dateRemainder:
            todayStr="Today!- "
            colour="red"
        else:
            if todaysDate==(dateRemainder-timedelta(days=1)):
                colour="yellow"
            todayStr=""
        return (colour,todayStr)
    def formatLabel(self,todayStr,label,dateReminder,colour):
        if str(type(label[2]))=="<class 'NoneType'>":
            rep="_None"
        else:
            rep=label[2]
        
        if label in self.sessionAddedRem:
            l=tk.Label(self,text=todayStr+"*Reminder: "+label[0]+", on the date: "+str(dateReminder)+", repeats every: "+rep+" days",bg=colour)
        else:
            l=tk.Label(self,text=todayStr+"Reminder: "+label[0]+", on the date: "+str(dateReminder)+", repeats every: "+rep+" days",bg=colour)
        return l
    def calculateCurrentRep(self,rep,startDate,todaysDate):
        #print(str(type(rep)))
        if(rep!="None" and str(type(rep))!="<class 'NoneType'>"):
            delta=todaysDate-startDate# if this is negative that means we shall return the start date because we do not need to repeat it and is good to be displayed
            rep=int(rep)
            if delta.days<0:
                return startDate
            else:
                daysBetween=delta.days#include the start date too
                if daysBetween==0:
                    return startDate#they are the same so we shall return the reminder to be for today as well
                #print("daysbetween:"+str(daysBetween))
                #print(str(startDate)+", "+str(todaysDate))
                todaysDateIndex=daysBetween%rep# if start date is 2, rep=3 and we are in 6th then the index shall be 1
                

                if todaysDateIndex!=0:# assuming it will never be negative
                    noDaysLeft=rep-todaysDateIndex
                else:
                    noDaysLeft=0
                #print("noDaysLeft:"+str(noDaysLeft))
                newDate=startDate+timedelta(days=daysBetween+noDaysLeft)
                return newDate
        else:
            return startDate
    def initialize_remainders(self):
        self.lastRemainderOnRow=0
        self.rowLabels=[]
        self.removeButtons=[]
        #print(self.parent.db.rem)
        if str(type(self.parent.db.rem))!="<class 'NoneType'>":
            todaysTime=datetime.now()
            todaysDate=todaysTime.date()
            for label in self.parent.db.rem:
                #print(label)
                dateRemainder = datetime.strptime(label[1],"%d/%m/%Y").date()
                dateRemainder = self.calculateCurrentRep(label[2],dateRemainder,todaysDate)
                if(todaysDate<=dateRemainder):
                    colour, todayStr=self.checkColourToUse(todaysDate,dateRemainder)
                    l=self.formatLabel(todayStr,label,dateRemainder,colour)
                    l.grid(row=self.lastRemainderOnRow,column=3)
                    self.rowLabels.append(l)
                    
                    b=tk.Button(self,text="Remove",command=lambda index=self.lastRemainderOnRow,remStr=label[0], dd=label[1], rep=label[2]:self.deleteReminder(index,remStr,dd,rep))
                    self.removeButtons.append(b)
                    self.removeButtons[len(self.removeButtons)-1].grid(row=self.lastRemainderOnRow,column=4)
                
                    self.lastRemainderOnRow=self.lastRemainderOnRow+1
    def deleteReminder(self,index,desc,due_date,repetition):
        self.parent.db.remove_reminder(desc,due_date,repetition)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line1="    x "+desc+", added for the time:"+due_date+", with repetition:"+str(repetition)+", was removed at:"+dt_string+"\n"
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

                    
