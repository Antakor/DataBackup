from datetime import date
import os
import platform
from copy import deepcopy


class Database():
    def __init__(self):
        if platform.system() == "Windows":
            self.location = str(os.path.dirname(os.path.realpath(__file__)) + "\\backupdatabase.txt")
        elif platform.system() == "Linux":
            self.location = str(os.path.dirname(os.path.realpath(__file__)) + "/backupdatabase.txt")
        else:
            print("You are using an unsupported operating system. The Programm will stop now.")
            quit()
        if os.path.isfile(self.location) == True:
            pass
        else:
            self.createfile()
        __filecontent = self.readfile()
        __filecontent = __filecontent.split("\n")
        del __filecontent[-1]
        for element in range(0, len(__filecontent)):
            __filecontent[element] = __filecontent[element].split("\t")
        for element in range(0, len(__filecontent)):
            __filecontent[element][0] = __filecontent[element][0].split("-")
        self._Content = __filecontent

    def createfile(self):
        __file = open(self.location, mode="w")
        __file.close()

    def readfile(self):
        __file = open(self.location, mode="r")
        __fileContent = __file.read()
        __file.close()
        return __fileContent

    def save(self):
        __tosave = deepcopy(self._Content)
        for element in range(0, len(__tosave)):
            __tosave[element][0] = str(__tosave[element][0][0] + "-" + __tosave[element][0][1] + "-" +__tosave[element][0][2])
        for element in range(0, len(__tosave)):
            __tosave[element] = str(__tosave[element][0] + "\t" +__tosave[element][1] + "\t" + __tosave[element][2] + "\n")
        __tosave = "".join(__tosave)
        __DB = open(self.location, mode="w")
        __DB.write(__tosave)
        __DB.close()

    def getContent(self):
        return self._Content

    def addContent(self, __date, __source, __dest):
        __date = str(__date)
        __date = __date.split("-")
        __toadd = [__date, __source, __dest]
        self._Content.append(__toadd)


DB = Database()