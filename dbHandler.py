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
        creation_date text) 
        ''')

    def create_tables(self):
        self.create_reminder_table()
    def add_reminder_to_table(self,desc,due_date,creation_date):
        if self.getSReminder(desc,due_date)==[]:
            item=(desc,due_date,creation_date)
            self.cursorSystemDatabase.execute('''INSERT INTO
                                            Reminder(description,
                                            due_date,
                                            creation_date) values (?,?,?)''',item)
            self.commit()
            self.select_all_reminders()#updating the reminders list
            return True#as in we did append to the db
        return False
    def remove_reminder(self,desc,due_date):
        self.cursorSystemDatabase.execute('''DELETE FROM
                                        Reminder WHERE description=? AND due_date=?''',(desc,due_date,))
        self.commit()
        self.select_all_reminders()
    def select_all_reminders(self):
        self.cursorSystemDatabase.execute('''SELECT description,due_date from Reminder ORDER BY ID_reminder DESC''')#order desc to ensure we show the most recent added ones
        self.rem=self.cursorSystemDatabase.fetchall()
    def getSReminder(self,desc,due_date):
        self.cursorSystemDatabase.execute('''SELECT description,due_date from Reminder WHERE
                                                description=? AND due_date=?''',(desc,due_date,))
        selRem=self.cursorSystemDatabase.fetchall()
        return selRem
    def closedb(self): 
        self.cursorSystemDatabase.close() 
        self.SystemDatabase.close()
    def commit(self):
        self.SystemDatabase.commit()

