from datetime import date
import os
import platform


class Database():
    def __init__(self):
        if platform.system() == "Windows":
            self.location = str(os.path.dirname(os.path.realpath(__file__)) + "\\backupdatabase.txt")
        elif platform.system() == "Linux)":
            self.location = str(os.path.dirname(os.path.realpath(__file__)) + "/backupdatabase.txt")
        else:
            print("You are using an unsupported operating system. The Programm will end")
            quit()
        if os.path.isfile(self.location) == True:
            pass
        else:
            self.createfile()

    def createfile(self):
        _DB = open(self.location, mode="w")
        _DB.close()

    def read(self):
        _DB = open(self.location, mode="r")
        _DBcontent = _DB.read()
        _DB.close()
        return _DBcontent

    def save(self, _DBcontent):
        _DB = open(self.location, mode="w")
        _DB.write(str(_DBcontent))
        _DB.close()


DB = Database()
lastbackup = str(date.today())
Content = str(lastbackup + "\n" + lastbackup + "\n")
DB.save(Content)
print(DB.read())