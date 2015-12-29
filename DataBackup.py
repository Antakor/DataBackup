import datetime
import os
from copy import deepcopy
import shutil


class Database:
    """All functions for the backupdatabase.txt"""
    def __init__(self):
        """Init of Database

        __location -- path of the backupdatabase
        __Content -- Contents of backupdatabase reformated as a list
        """
        self.__filenameofdb = "backupdatabase"

        self.__location = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.__filenameofdb)

        if os.path.isfile(self.__location):
            pass
        else:
            self.createfile()

        self.__Content = self.readfile()
        for element in range(0, len(self.__Content)):
            __src = self.__Content[element][1]
            __dst = self.__Content[element][2]
            if os.path.isdir(__src):
                self.checkdirs(__src, __dst)

    def checkdirs(self, __src, __dst):
        __Content = os.listdir(__src)
        for element in __Content:
            __srcnew = os.path.join(__src, element)
            __dstnew = os.path.join(__dst, element)
            if os.path.isdir(__srcnew):
                self.checkdirs(__srcnew, __dstnew)
            elif os.path.isfile(__srcnew):
                if self.posofsrcindb(__srcnew) == []:
                    self.addcontent(__srcnew, __dst)
            else:
                pass

    def createfile(self):
        """creates database .txt if not existant"""
        __file = open(self.__location, mode="w")
        __file.close()

    def readfile(self):
        """reads content of backupdatabase.txt, reformats the string as a list and saves it to self.__Content"""
        __file = open(self.__location)
        __filecontent = __file.read()
        __file.close()
        __filecontent = __filecontent.split("\n")
        del __filecontent[-1]
        for element in range(0, len(__filecontent)):
            __filecontent[element] = __filecontent[element].split("\t")
        for element in range(0, len(__filecontent)):
            __filecontent[element][0] = __filecontent[element][0].split("-")
        return __filecontent

    def savetofile(self):
        """writes content to database file"""
        __tosave = self.formattostring()
        __DB = open(self.__location, mode="w")
        __DB.write(__tosave)
        __DB.close()

    def getcontent(self):
        return self.__Content

    def addcontent(self, __src, __dst):
        """adds things to self.__Content
        """
        __date = str(datetime.date.today())
        __date = __date.split("-")
        __toadd = [__date, __src, __dst]
        self.__Content.append(__toadd)

    def posofsrcindb(self, __src):
        """checks if a source is in self.__Content

        __src - path of source
        """
        __position = []
        for element in range(0, len(self.__Content)):
            if self.__Content[element][1] == __src:
                __position.append(element)
        return __position

    def removecontent(self, __position):
        if not __position:
            pass
        else:
            for element in range(0, len(__position)):
                del self.__Content[int(__position[element])]

    def formattostring(self):
        __toformat = deepcopy(self.__Content)
        for element in range(0, len(__toformat)):
            __toformat[element][0] = \
                str(__toformat[element][0][0] + "-" + __toformat[element][0][1] + "-" + __toformat[element][0][2])
        for element in range(0, len(__toformat)):
            __toformat[element] = \
                str(__toformat[element][0] + "\t" + __toformat[element][1] + "\t" + __toformat[element][2] + "\n")
        __toformat = "".join(__toformat)
        return __toformat


class Backup:
    def __init__(self):
        self.__deltat = 7
        self.__today = datetime.date.today()
        self.__filesindb = DB.getcontent()
        self.__objectstobackup = []
        self.autobackup()

    def autobackup(self):
        """searches for files in the database, wich were'nt backupped in 7 days"""
        __filestocheck = self.__filesindb
        for element in range(0, len(__filestocheck)):
            __yofelement = int(__filestocheck[element][0][0])
            __mofelement = int(__filestocheck[element][0][1])
            __dofelement = int(__filestocheck[element][0][2])
            __datelastbackup = datetime.date.today()
            __datelastbackup = __datelastbackup.replace(year=__yofelement, month=__mofelement, day=__dofelement)
            __delta = self.__today - __datelastbackup
            if __delta.days >= self.__deltat and os.path.isfile(__filestocheck[element][1]):
                self.__objectstobackup.append(element)

    def backupnew(self):
        """searches for files in the database, wich were'nt backupped in 7 days"""
        __filestocheck = self.__filesindb
        for element in range(0, len(__filestocheck)):
            __yofelement = int(__filestocheck[element][0][0])
            __mofelement = int(__filestocheck[element][0][1])
            __dofelement = int(__filestocheck[element][0][2])
            __datelastbackup = datetime.date.today()
            __datelastbackup = __datelastbackup.replace(year=__yofelement, month=__mofelement, day=__dofelement)
            __delta = self.__today - __datelastbackup
            if __delta.days == 0 and os.path.isfile(__filestocheck[element][1]):
                self.__objectstobackup.append(element)

    def dobackup(self):
        """performs the backup"""
        for element in range(0, len(self.__objectstobackup)):
            __src = self.__filesindb[self.__objectstobackup[element]][1]
            __dst = self.__filesindb[self.__objectstobackup[element]][2]
            if os.path.isfile(__src):
                if not os.path.exists(__dst):
                    os.makedirs(__dst)
                shutil.copy(__src, __dst)
                DB.addcontent(__src, __dst)
            else:
                print("the following path is corrupt: " + __src)
        DB.removecontent(self.__objectstobackup)
        self.__objectstobackup = []


def addnew():
    while True:
        __src = input("Source Path:")
        if DB.posofsrcindb(__src):
            print("The source you entered is in the list.")
            break
        else:
            if os.path.exists(__src):
                __dst = input("Destination Path:")
                DB.addcontent(__src, __dst)
                if os.path.isdir(__src):
                    DB.checkdirs(__src, __dst)
                DB.savetofile()
                BU.backupnew()
                BU.dobackup()
                break
            else:
                print("you have not entered a valid path as source")

DB = Database()
BU = Backup()
BU.dobackup()
print("Datasaver\n")
print("Welcome to Datasaver. Datasaver is little programm to do backups.")
print("You can add a new entry to the database")
print("If you want to add an entry to your backup list type: \"add\".")
print("To quit the programm type: \"end\".")
while True:
    userin = input("What do you want to do?: ")
    if userin == "add":
        addnew()
    elif userin == "end":
        BU.dobackup()
        quit()
    else:
        print("you have not typed a valid option. try checking your spelling.")
