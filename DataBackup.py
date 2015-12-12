import datetime
import os
import platform
from copy import deepcopy
import shutil


class Database():
    """All functions for the Database.txt    """
    def __init__(self):
        """Init of Database

        __location -- path of the backupdatabase.txt
        __Content -- Contents of backupdatabase.txt reformated as a list
        """
        if platform.system() == "Windows":
            self.__location = str(os.path.dirname(os.path.realpath(__file__)) + "\\backupdatabase.txt")
        elif platform.system() == "Linux":
            self.__location = str(os.path.dirname(os.path.realpath(__file__)) + "/backupdatabase.txt")
        else:
            print("You are using an unsupported operating system. The Programm will stop now.")
            quit()
        if os.path.isfile(self.__location) == True:
            pass
        else:
            self.createfile()

        self.__Content = self.readfile()

    def createfile(self):
        __file = open(self.__location, mode="w")
        __file.close()

    def readfile(self):
        __file = open(self.__location, mode="r")
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
        __tosave = deepcopy(self.__Content)
        for element in range(0, len(__tosave)):
            __tosave[element][0] = str(__tosave[element][0][0] + "-" + __tosave[element][0][1] + "-" + __tosave[element][0][2])
        for element in range(0, len(__tosave)):
            __tosave[element] = str(__tosave[element][0] + "\t" + __tosave[element][1] + "\t" + __tosave[element][2] + "\n")
        __tosave = "".join(__tosave)
        __DB = open(self.__location, mode="w")
        __DB.write(__tosave)
        __DB.close()

    def getcontent(self):
        return self.__Content

    def addcontent(self, __date, __src, __dst):
        __date = str(__date)
        __date = __date.split("-")
        __toadd = [__date, __src, __dst]
        self.__Content.append(__toadd)

    def srcinlist(self, __src):
        __position = []
        for element in range(0, len(self.__Content)):
            if self.__Content[element][1] == __src:
                __position.append(element)
        return __position

    def removecontent(self, __src):
        __position = self.srcinlist(__src)
        if not __position:
            pass
        else:
            for element in range(0, len(__position)):
                del self.__Content[int(__position[-1])]
                del __position[-1]


class backup():
    def __init__(self):
        self.__today = datetime.date.today()
        self.__filestobackup = self.auto()

    def auto(self):
        __filestobackup = []
        __filestocheck = DB.getcontent()
        for element in range(0, len(__filestocheck)):
            __yearofelement = int(__filestocheck[element][0][0])
            __monthofelement = int(__filestocheck[element][0][1])
            __dayofelement = int(__filestocheck[element][0][2])
            __datelastbackup = datetime.date.today()
            __datelastbackup = __datelastbackup.replace(year=__yearofelement, month=__monthofelement, day=__dayofelement)
            __delta = self.__today - __datelastbackup
            if __delta.days >= 7:
                __filestobackup.append(__filestocheck[element])
        return __filestobackup

    def dobackup(self):
        while len(self.__filestobackup) != 0:
            __src = self.__filestobackup[0][1]
            if os.path.isdir(__src):
                __dst = self.__filestobackup[0][2]
                shutil.copytree(__src, __dst, symlinks=False, ignore=None, ignore_dangling_symlinks=True)
                del self.__filestobackup[0]
            elif os.path.isfile(__src):
                __dst = self.__filestobackup[0][2]
                shutil.copy(__src, __dst)

DB = Database()
BU = backup()