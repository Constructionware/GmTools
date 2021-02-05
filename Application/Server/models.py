#models.py
#GMtools Models
import json
import datetime
import requests 

from Server.server import cnf
from Server.dataBase import Database

credo = 'gmtools:gxcityx776'
class Tool:
    id:str = None
    name:str = None
    brand:str = None
    tool_type:str = None
    category:str = None
    supplier:str = cnf.TITLE
    specification:dict = {
        "power": {
            "source": None,
            "volts": 0,
            "current": 0,
            "cycle": 0
        },
        "props": []        
    }
    cost:dict = {
        "usd": 0.0,
        "jad": 0.0
    }
    available:bool = False
    condition:list = []
    listed:bool = False
    url:str = f'http://{credo}@localhost:5984/gmtools'
    images_url:list = []




    def __init__(self, name:str=None, id:str=None):
        if name:
            self.name = name
            self.generateId
        if id:
            self.getTool(id)

    @property
    def generateId(self):
        self.id = cnf.keygen.name_id(self.supplier, self.name)

    def getTool(self, tool_id):
        tool = requests.get(f"{self.url}/{tool_id}")
        print(tool)   

    @property
    def getTools(self):
        tools = requests.get(f"{self.url}/_design/tools/_view/index").json()
        print(tools)             



