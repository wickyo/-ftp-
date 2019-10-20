from db import db_handler
class BASE:
    def save(self):
        db_handler.save(self)

    @classmethod
    def select(cls,name):
        obj = db_handler.select(cls,name)
        return obj

class User(BASE):
    def __init__(self,name,pwd):
        self.name = name
        self.pwd = pwd
        self.file_list = []
        self.save()

    def upload_file(self,file_name):
        File(file_name)
        self.file_list.append(file_name)
        self.save()


class File(BASE):
    def __init__(self,name):
        self.name = name
        self.save()