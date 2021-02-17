#models.py
#GMtools Models

import json
import datetime
import math
import requests 
from PIL import Image

from Server.dataBase import cnf
from Server.dataBase import (Category, BatteryTool, FuelTool, PowerTool)
from Server.dataBase import ( Supplier, Client, SalesAgent )
from Server.dataBase import ( Account, Supply, Sale )

credo = 'gmtools:gxcityx776'

def register(tool:str=None, data:dict=None):
    registry = {
        "battery": BatteryTool(name=data['name']),
        "fuel": FuelTool(name=data['name']),
        "power": PowerTool(name=data['name'])
    }
    return registry.get(tool, None)


class Tool:
    ''' Requires a tool type " battery, fuel, power" 
    Init a selected Tool object.'''
    id:str = None
    name:str = None
    brand:str = None
    type:str = None
    specification:dict = {}
    price:dict = {
        "usd": 0.0,
        "jad": 0.0
    }
    data:dict = dict(
        category = None,
        instock = 0,
        condition = None,
        url=None,
        images_urls = [],
        supplier=None,
        supply_date=datetime.datetime.now(),
        updated=datetime.datetime.now(),
        created_by=None,
        updated_by=None 

    )

    def __init__(self, id:str=None, name:str=None, type:str=None):
        if name:
            self.name = name
        if name and id and type:
            self.id=id
            self.name=name
            self.type=type
            self.getTool(id=id, tool_type=type)
            

    def getTool(self, id:str=None, tool_type:str=None):
        self.tool = register(tool=tool_type, data={"id": id})
        
        

    @property
    def getTools(self):
        tools = requests.get(f"{self.url}/_design/tools/_view/index").json()
        print(tools) 

     
            
    def processImage(self, uri:str=None):
        image = Image.open(uri)
        x, y = image.size
        x2, y2 = math.floor(x-50, math.floor(y-20))
        image = image.resize((x2,y2), Image.ANTIALIAS)
        path= ""
        image.save(path, quality=20, optimize=True)

     



