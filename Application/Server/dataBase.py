#dataBase.py
import datetime
import dataset

import os
import json

class Database:
    name:str = None
    default:str = 'gmt-power.sqlite'
    user:str = None
    dbs:dict = {
        "power":'gmt-power.sqlite', 
        "battery": 'gmt-battery.sqlite'
    }
    location:str = os.path.realpath("D:/GmtDB")

    def __init__(self, name:str=None):
        self.set_user
        if name:
            self.name = name            
            self.connect_db(self.name)
        else:
            self.connect_db(self.default)

    @property
    def set_user(self):
        self.user = os.getlogin()

    def connect_db(self, dbn:str=None):
        if dbn:
            handle = f"{self.location}/{self.dbs.get(dbn)}"
            self.connection = dataset.connect(handle)
            
            if dbn == "battery":
                self.default_table = "batterytool"
            else:
                self.default_table = "powertool"
    
    @property
    def close_connection(self):
        self.connection.close()

    @property
    def create_table(self):
        # Create table
        self.table = self.connection[self.default_table]

    def save(self, data:dict=None):
        if data:
            self.table.insert(data)
            return {"success": True}
        else:
            return {"success": False}




    def __repr__(self):
        if self.name:
            return f"GM Tools Sqlite Database {self.name}"
        else:
            return f"GM Tools Default Sqlite Database {self.default}"



db = Database(name='battery')

#print(db.connection)
print(db)
db.create_table
db.close_connection
#print(dir(os))
