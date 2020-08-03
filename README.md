**Version 1.4.0**

A Python 3.8 program which will be tracking the number of unproductive and productive actions which 
you are doing based on a score. The more productive you are the more positive the app message will be.
The aim is to have 0 or more productive points. You can add productive or unproductive points by the use of the
GUI buttons. All the history will be tracked inside a log file called "logGames.txt", this will include the
time you added each entry of points.

Case scenario example:
1. You play a quick match in your game.
1. You click add a quick game match related button.
1. You do a long subject read.
1. You click the relevant button.
1. You check your score.


(Windows users)Make sure you have Python 3.8 in your PATH var as "python", otherwise change the bat file accordingy.


Another thing to mention is that the txt file will only be updated after you closed the application. In
order to check the current state of "logGames.txt" check your console. 

If you force kill the app or shutdown your computer while the app runs the data input in the particular session the txt may get corrupted!

I shall tell you that the app does not autoupdate when the day changes. So I reccomend you closing it and opening it again if you
will be transiting to the next day for the confusion avoidance.

If you click remove on a reminder you will remove it from the database. You do not need to delete it! When its start date passes the reminder won't show anymore.

## Contributors

- Valentin I Burlacu <blxyon@yahoo.com>

---
## Updates

(V1.4.0)
- The repetition of certain reminders in a number of days interval. e.g.: I would like to be running at a 
period of 2 days begining from tommorow. I will be setting the date to be tommorows date and set the day period
to 2. The program shall tell you that you begin the running tommorow and it will be repeatedly tell you this
after each 2 days.
- Database structure has changed by adding a new column
- The program calculates each time it is opened how many days untill the next activity that you are due to be doing
by the reminders.
- In the reminders section you may see None and _None. None is for empty cell while _None is for None being displayed in the cell

(V1.3.1)
- Colours ilustrating the most appropriate due reminders. 
A reminder being red means it is due today and if it is yellow it is due tommorow.
Otherwise it will be white.

(V1.3.0) 
- Reminders manager deleting and database link functionality to enhance functionality.
- Text document structure changed for better visualisation
- New reminders added have an asterisk in the beginning for visualistion

(V1.2.0) Reminders manager added

(V1.1.0) Transformed it into oop with more functionality buttons (+6,+4...) (-6,-4...)

(V1.0.0) Basic (+1) (-1) points app 

## License & copyright

(c) Valentin I Burlacu, learningMatches

Licensed under the [MIT LICENSE](LICENSE)