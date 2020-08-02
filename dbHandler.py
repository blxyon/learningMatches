import sqlite3 

#beacuse we are caching inside this class I would like that the caches are updating
#inside the instance of the DatabaseApp

class DatabaseApp:
    def __init__(self,*args,**kwargs):
        self.SystemDatabase=sqlite3.connect("leMa.db") 
        self.cursorSystemDatabase=self.SystemDatabase.cursor()
        self.create_tables()
        self.select_all_reminders()#caching the reminders...
    def create_reminder_table(self): 
        self.cursorSystemDatabase.execute('''CREATE TABLE IF NOT EXISTS Reminder 
        (ID_reminder integer PRIMARY KEY, 
        description text, 
        due_date text, 
        creation_date text,
        days_repetition text) 
        ''')

    def create_tables(self):
        self.create_reminder_table()
    def add_reminder_to_table(self,desc,due_date,creation_date,repetition):
        if self.getSReminder(desc,due_date,repetition)==[]:
            item=(desc,due_date,creation_date,repetition)
            self.cursorSystemDatabase.execute('''INSERT INTO
                                            Reminder(description,
                                            due_date,
                                            creation_date,
                                            days_repetition) values (?,?,?,?)''',item)
            self.commit()
            self.select_all_reminders()#updating the reminders list
            return True#as in we did append to the db
        return False
    def remove_reminder(self,desc,due_date,repetition):
        #print(self.getSReminder(desc,due_date,repetition))
        if repetition!=None:#this solves the earlier app versions problems where they would have an empty cell in the days_repetition column
            self.cursorSystemDatabase.execute('''DELETE FROM
                                        Reminder WHERE description=? AND due_date=? AND days_repetition=?''',(desc,due_date,repetition))
        else:
            self.cursorSystemDatabase.execute('''DELETE FROM
                                        Reminder WHERE description=? AND due_date=? AND days_repetition is NULL''',(desc,due_date))
        self.commit()
        self.select_all_reminders()
    def select_all_reminders(self):
        self.cursorSystemDatabase.execute('''SELECT description,due_date,days_repetition from Reminder ORDER BY ID_reminder DESC''')#order desc to ensure we show the most recent added ones
        self.rem=self.cursorSystemDatabase.fetchall()
    def getSReminder(self,desc,due_date,repetition):
        self.cursorSystemDatabase.execute('''SELECT description,due_date from Reminder WHERE
                                                description=? AND due_date=? AND days_repetition=?''',(desc,due_date,repetition,))
        selRem=self.cursorSystemDatabase.fetchall()
        return selRem
    def closedb(self): 
        self.cursorSystemDatabase.close() 
        self.SystemDatabase.close()
    def commit(self):
        self.SystemDatabase.commit()

