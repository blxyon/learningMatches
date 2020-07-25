from datetime import datetime
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
        curYear=getCurrentTimeToList()[2]
        monthOptions = ["Month","1","2","3","4","5","6","7","8","9","10","11","12"]
        yearOptions =[curYear,str(int(curYear)+1),str(int(curYear)+2),str(int(curYear)+3),str(int(curYear)+4)]
        dayOptions=["Select Month"]

        self.addRemainderButton=tk.Button(self,text="Add remainder",command=lambda:self.add_remainder())
        self.addRemainderButton.grid(row=2,column=0)
        
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
    def add_remainder(self):
        month=self.remainderMonth.get()
        if(month!="Month"):
            year=self.remainderYear.get()
            day=self.remainderDay.get()
            reminderStr=self.remainderVar.get()
            if(reminderStr==""):
                remainderStr="_not_specified"
            now = datetime.now()
            todaysDate=now.date()
            dt_string = ("%s/%s/%s"%(day,month,year,))#string format
            line1="Reminder for:"+reminderStr+", added for the time:"+dt_string+"\n"
            self.parent.txt.writeAndDisplay(line1)
            todaysDateString=("%s/%s/%s"%(getCurrentTimeToList()[0],getCurrentTimeToList()[1],getCurrentTimeToList()[2],))
            self.parent.db.add_reminder_to_table(reminderStr,dt_string,todaysDateString)

            #we must update the gui.. if necessary
            dateRemainder = datetime.strptime(dt_string,"%d/%m/%Y").date()
            if(todaysDate<=dateRemainder):
                l=tk.Label(self,text="Activity: "+reminderStr+", on the date: "+dt_string)
                l.grid(row=self.lastRemainderOnRow,column=3)
                self.lastRemainderOnRow=self.lastRemainderOnRow+1
    def initialize_remainders(self):
        self.lastRemainderOnRow=0
        print(self.parent.db.rem)
        if str(type(self.parent.db.rem))!="<class 'NoneType'>":
            todaysTime=datetime.now()
            todaysDate=todaysTime.date()
            for label in self.parent.db.rem:
                dateRemainder = datetime.strptime(label[1],"%d/%m/%Y").date()         
                if(todaysDate<=dateRemainder):
                    l=tk.Label(self,text="Activity: "+label[0]+", on the date: "+label[1])
                    l.grid(row=self.lastRemainderOnRow,column=3)
                    self.lastRemainderOnRow=self.lastRemainderOnRow+1
    
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

                    
