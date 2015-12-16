import datetime
import os
import platform
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
        if platform.system() == "Windows":
            self.__location = str(os.path.dirname(os.path.realpath(__file__)) + "\\" + str(self.__filenameofdb))
        elif platform.system() == "Linux":
            self.__location = str(os.path.dirname(os.path.realpath(__file__)) + "/" + str(self.__filenameofdb))
        else:
            print("You are using an unsupported operating system. The Programm will stop now.")
            quit()
        if os.path.isfile(self.__location):
            pass
        else:
            self.createfile()

        self.__Content = self.readfile()

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

    def addcontent(self, __date, __src, __dst):
        """adds things to self.__Content
        """
        __date = str(__date)
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
        self.__objectstobackup = self.auto()


    def auto(self):
        """searches for files in the database, wich were'nt backupped in 7 days"""
        __objectstobackup = []
        __filestocheck = self.__filesindb
        for element in range(0, len(__filestocheck)):
            __yofelement = int(__filestocheck[element][0][0])
            __mofelement = int(__filestocheck[element][0][1])
            __dofelement = int(__filestocheck[element][0][2])
            __datelastbackup = datetime.date.today()
            __datelastbackup = __datelastbackup.replace(year=__yofelement, month=__mofelement, day=__dofelement)
            __delta = self.__today - __datelastbackup
            if __delta.days >= self.__deltat and os.path.isfile(__filestocheck[element][1]):
                __objectstobackup.append(element)
        return __objectstobackup

    def dobackup(self):
        """performs the backup"""
        for element in range(0, len(self.__objectstobackup)):
            __src = self.__filesindb[self.__objectstobackup[element]][1]
            __dst = self.__filesindb[self.__objectstobackup[element]][2]
            if os.path.isdir(__src):
                shutil.copytree(__src, __dst, symlinks=False)
                DB.addcontent(str(self.__today), __src, __dst)
            elif os.path.isfile(__src):
                if not os.path.exists(__dst):
                    os.makedirs(__dst)
                shutil.copy(__src, __dst)
                DB.addcontent(str(self.__today), __src, __dst)
            else:
                print("the following path is corrupt: " + __src)
        DB.removecontent(self.__objectstobackup)


DB = Database()
BU = Backup()


def addnewentry():
    __src = input("Source Path:")
    __dst = input("Destination Path:")
    __date = str(datetime.date.today())
    DB.addcontent(__date, __src, __dst)
