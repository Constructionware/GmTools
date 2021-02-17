#dataBase.py

import os
import json
import time
#import dataset
import databases
#import sqlite3

from sqlalchemy import *
from sqlalchemy.ext import mutable
from sqlalchemy import orm
from sqlalchemy.ext import declarative
from Server.server import cnf


class JsonEncodedDict(TypeDecorator):
  """Enables JSON storage by encoding and decoding on the fly."""
  impl = String

  def process_bind_param(self, value, dialect):
    return json.dumps(value)

  def process_result_value(self, value, dialect):
    return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)

Base = declarative.declarative_base()
AdminBase = declarative.declarative_base()


class Database:
    name:str = None
    default:str = 'tools'
    user:str = None    
    location:str = os.path.realpath("D:/GmtDB")

    def __init__(self, name:str=None):
        self.set_user
        if name:
            self.connect_db(name)
            self.create_db_session
        else:
            self.connect_db(self.default)
            self.create_db_session            

    @property
    def set_user(self):
        self.user = os.getlogin()

    def connect_db(self, dbn:str=None):
        if dbn:
            self.name = cnf.SQL_DATABASE_URI.get(dbn)
            self.engine = create_engine(self.name, echo=True) 
            # an async connector 
            self.async_connection = databases.Database(self.name)
    
    @property
    def close_connection(self):
        self.async_connection.disconnect()

    @property
    def create_tools_table(self):        
        Base.metadata.bind = self.engine
        Base.query = self.session.query_property()
        Base.metadata.create_all()
    
    @property
    def create_admin_table(self):        
        AdminBase.metadata.bind = self.engine
        AdminBase.query = self.session.query_property()
        #Base.query = self.session.query_property()
        AdminBase.metadata.create_all()

    @property
    def create_db_session(self):
        self.session = orm.scoped_session(orm.sessionmaker(autocommit=False,
                                                            autoflush=false,
                                                            bind=self.engine))

    def __repr__(self):
        if self.name:
            return f"GM Tools Sqlite Database {self.name}"
        else:
            return f"GM Tools Default Sqlite Database {self.dbs.get(self.default)}"


class Client(AdminBase):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    client_id = Column(String, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    data = Column(JsonEncodedDict)
    
    def __init__(self, firstname:str=None, lastname:str=None, client_id:str=None, directive:str=None):
        if firstname and lastname and directive=='new':
            self.firstname = firstname
            self.lastname = lastname
            self.generate_id()
            self.connect_db

        if firstname and lastname and directive=='search':
            self.firstname = firstname
            self.lastname = lastname
            self.connect_db
            self.search(f"firstname-lastname")
            # Search for  the purchaser's data by name method
        if client_id:
            self.client_id = client_id
            self.connect_db
            
            # Get the purchaser's data by id method
        # Connect the database anyway
        self.connect_db

    
    def generate_id(self):
        if self.firstname and self.lastname:
            self.client_id = cnf.keygen.name_id(self.firstname, self.lastname)
                
    @property
    def connect_db(self):
        self.db = Database(name='admin')

    @property
    async def list_purchasers(self):
        query = """SELECT * FROM client"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.purchasers_list:list = []
        self.purchasers_index:list = []
        for item in results:
            self.purchasers_list.append({
                "id": item[1],
                "firstname": item[2],
                "lastname": item[3],
                "data": json.loads(item[4])                
            })
            self.purchasers_index.append(
                {
                    "id": item[1],
                    "name": f"{item[2]} {item[3]}"                
                }
            )   
        return self.purchasers_index

    @property
    async def get(self):
        query = "SELECT * FROM client WHERE client_id = :client_id"
        await self.db.async_connection.connect()
        result = await self.db.async_connection.fetch_one(query=query, values={"client_id": self.client_id})    
        await self.db.async_connection.disconnect()
        return result

    async def get_by_id(self, id):
        query = "SELECT * FROM client WHERE client_id = :client_id"
        await self.db.async_connection.connect()
        result = await self.db.async_connection.fetch_one(query=query, values={"client_id": id})    
        await self.db.async_connection.disconnect()
        return result

    def search(self, term:str=None):
        if term:
            term = term.spilt('-')
            # Implement search mechanism.
            return term
        return {"message": "You did not provide a Search Term."}

    @property
    def save(self):
        self.db.session.add(self)
        self.db.session.commit()
    

class Supplier(AdminBase):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True)
    supplier_id = Column(String, nullable=False)
    name = Column(String)
    data = Column(JsonEncodedDict)
    
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.generate_id()
            self.connect_db
        self.connect_db
    
    def generate_id(self):
        if self.name:
            self.supplier_id = cnf.keygen.name_id(cnf.TITLE, self.name)            
    
    @property
    def connect_db(self):
        self.db = Database(name='admin')
    
    async def list_suppliers(self):
        query = """SELECT * FROM supplier"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.suppliers_list:list = []
        self.suppliers_index:list = []
        for item in results:
            self.suppliers_list.append({
                "id": item[1],
                "name": item[2],
                "data": json.loads(item[3])                
            })
            self.suppliers_index.append(
                {
                    "id": item[1],
                    "name": f"{item[2]} {item[3]}"                
                }
            )
        return self.supplers_index

    @property
    def save(self):        
        self.db.session.add(self)
        self.db.session.commit()


class SalesAgent(AdminBase):
    __tablename__ = 'sales-agent'
    id = Column(Integer, primary_key=True)
    agent_id = Column(String, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    data = Column(JsonEncodedDict)
    
    def __init__(self, firstname:str=None, lastname:str=None):
        if firstname and lastname:
            self.firstname = firstname
            self.lastname = lastname
            self.generate_id()
            self.connect_db
        self.connect_db
    
    def generate_id(self):
        self.agent_id = cnf.keygen.name_id(self.firstname, self.lastname)            
    
    @property
    def connect_db(self):
        self.db = Database(name='admin')

    async def list_agents(self):
        query = """SELECT * FROM sales-agent"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.sales_agents_list:list = []
        self.sales_agents_index:list = []
        for item in results:
            self.sales_agents_list.append({
                "id": item[1],
                "firstname": item[2],
                "lastname": item[3],
                "data": json.loads(item[4])                
            })
            self.sales_agents_index.append(
                {
                    "id": item[1],
                    "name": f"{item[2]} {item[3]}"                
                }
            )        

    @property
    def save(self):        
        self.db.session.add(self)
        self.db.session.commit()
    
#-------- TOOL MODEL TYPES -------
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.connect_db
        self.connect_db

    @property
    def connect_db(self):
        self.db = Database(name='tools')

    async def list_category(self):
        query = """SELECT * FROM category"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        return results
        
    @property
    def save(self):
        self.connect_db
        self.db.session.add(self)
        self.db.session.commit()


class BatteryTool(Base):
    __tablename__ = 'battery_tool'    
    id = Column(Integer, primary_key=True)
    tool_id = Column(String(12), nullable=False)
    name = Column(String(100))
    brand = Column(String(60))
    type = Column(String(10)) 
    specification = Column(JsonEncodedDict) 
    price = Column(JsonEncodedDict)
    data = Column(JsonEncodedDict)
    image_url = "/tools/static/images/Batterytools/" 
    
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.type = 'battery'           
            self.generate_id
            self.connect_db
        self.connect_db

    
    @property
    def generate_id(self):
        if self.name:
            self.tool_id = cnf.keygen.name_id('B', self.name)

    async def list_tools(self):
        query = """SELECT * FROM battery_tool"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.inventory:list = []
        self.tool_index:list = []
        for item in results:
            self.inventory.append({
                "id": item[1],
                "name": item[2],
                "brand": item[3],
                "type": item[4],
                "image_url": self.image_url,
                "specification": json.loads(item[5]),
                "price": json.loads(item[6]), 
                "data": json.loads(item[7])               
            })
            self.tool_index.append(
                {
                    "id": item[1],
                    "name": f"{item[2]} {item[3]}",
                    "brand": item[3],
                    "image_url": self.image_url,
                    "images": json.loads(item[7]).get('image_urls', None)                 
                }
            )       
        return self.tool_index
                
    @property
    def connect_db(self):
        self.db = Database(name='tools')

    def getTool(self, id:str=None):
        return BatteryTool.query.all()

    @property
    def save(self):
        self.connect_db
        self.db.session.add(self)
        self.db.session.commit()    


class PowerTool(Base):
    __tablename__ = 'power_tool'
    id = Column(Integer, primary_key=True)
    tool_id = Column(String, nullable=False)
    name = Column(String)
    brand = Column(String)
    type = Column(String) 
    specification = Column(JsonEncodedDict) 
    price = Column(JsonEncodedDict)
    data = Column(JsonEncodedDict)
    image_url = "/tools/static/images/Powertools/" 
    
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.type = 'power'
            self.generate_id
            self.connect_db
        self.connect_db

    
    @property
    def generate_id(self):
        if self.name:
            self.tool_id = cnf.keygen.name_id('P', self.name)
                
    @property
    def connect_db(self):
        self.db = Database(name='tools')

    async def list_tools(self):
        query = """SELECT * FROM power_tool"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.inventory:list = []
        self.tool_index:list = []
        for item in results:
            self.inventory.append({
                "id": item[1],
                "name": item[2],
                "brand": item[3],
                "type": item[4],
                "image_url": self.image_url,
                "specification": json.loads(item[5]),
                "price": json.loads(item[6]), 
                "data": json.loads(item[7])               
            })
            self.tool_index.append(
                {
                    "id": item[1],
                    "name": f"{item[2]} {item[3]}",
                    "brand": item[3],
                    "image_url": self.image_url,
                    "images": json.loads(item[7]).get('image_urls', None)   
                    
                                  
                }
            )       
        return self.tool_index

    @property
    def save(self):        
        self.db.session.add(self)
        self.db.session.commit() 

    def getTool(self, id:str=None):
        if id:
            tool = PowerTool.query.filter_by(tool_id=id).first()
            return tool
        return None 


class FuelTool(Base):
    __tablename__ = 'fuel_tool'
    id = Column(Integer, primary_key=True)
    tool_id = Column(String, nullable=False)
    name = Column(String)
    brand = Column(String)
    type = Column(String) 
    specification = Column(JsonEncodedDict) 
    price = Column(JsonEncodedDict)
    data = Column(JsonEncodedDict)
    image_url = "/tools/static/images/Fueltools/" 
    
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.type = 'fuel'
            self.generate_id
            self.connect_db
        self.connect_db
    
    @property
    def generate_id(self):
        if self.name:
            self.tool_id = cnf.keygen.name_id('F', self.name)
                
    @property
    def connect_db(self):
        self.db = Database(name='tools')

    async def list_tools(self):
        query = """SELECT * FROM fuel_tool"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.inventory:list = []
        self.tool_index:list = []
        for item in results:
            self.inventory.append({
                "id": item[1],
                "name": item[2],
                "brand": item[3],
                "type": item[4],
                "image_url": self.image_url,
                "specification": json.loads(item[5]),
                "price": json.loads(item[6]), 
                "data": json.loads(item[7])               
            })
            self.tool_index.append(
                {
                    "id": item[1],
                    "name": f"{item[2]} {item[3]}",
                    "brand": item[3],
                    "image_url": self.image_url,
                    "images": json.loads(item[7]).get('image_urls', None)              
                }
            )       
        return self.tool_index

    @property
    def save(self):
        self.db.session.add(self)
        self.db.session.commit()

    def getTool(self, id:str=None):
        return FuelTool.query.all()

#------- ACTIVITY ------------

class Supply(AdminBase):
    __tablename__ = 'supply'
    id = Column(Integer, primary_key=True)
    sid = Column(String, nullable=False)
    name = Column(String)
    data = Column(JsonEncodedDict)
    
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.generate_id()
            self.connect_db
        self.connect_db
    
    def generate_id(self):
        if self.name:
            self.supplier_id = cnf.keygen.name_id(cnf.TITLE, self.name)
               
    @property
    def connect_db(self):
        self.db = Database(name='admin')
    
    async def list_supplies(self):
        query = """SELECT * FROM supply"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.suppliers_list:list = []
        self.suppliers_index:list = []
        for item in results:
            self.suppliers_list.append({
                "id": item[1],
                "name": item[2],
                "data": json.loads(item[3])               
            })
            self.suppliers_index.append(
                {
                    "id": item[1],
                    "name": item[2],
                                                  
                }
            )       
        return self.suppliers_index

    @property
    def save(self):
        self.db.session.add(self)
        self.db.session.commit()    


class Sale(AdminBase):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    tid = Column(String, nullable=False)
    item = Column(JsonEncodedDict)
    data = Column(JsonEncodedDict)
    
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.generate_id()
            self.connect_db
        self.connect_db
    
    def generate_id(self):
        if self.name:
            self.tid = cnf.keygen.name_id(cnf.TITLE, self.item['name'])            
    
    @property
    def connect_db(self):
        self.db = Database(name='admin')

    async def list_sales(self):
        query = """SELECT * FROM sale"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.sales_list:list = []
        self.sales_index:list = []
        for item in results:
            self.sales_list.append({
                "id": item[1],
                "item": item[2],
                "data": json.loads(item[3])               
            })
            self.sales_index.append(
                {
                    "id": item[1],
                    "item": item[2]                                  
                }
            )       
        return self.sales_index

    @property
    def save(self):        
        self.db.session.add(self)
        self.db.session.commit()


class Account(AdminBase):
    __tablename__ = 'suppliers-accounts'
    id = Column(Integer, primary_key=True)
    aaid = Column(String, nullable=False)
    data = Column(JsonEncodedDict)
    transactions = Column(JsonEncodedDict)     
        
    def __init__(self, name:str=None):
        if name:
            self.name = name
            self.generate_id()
            self.connect_db
        self.connect_db

    
    def generate_id(self):
        if self.name:
            self.tid = cnf.keygen.name_id(cnf.TITLE, self.item['name'])
            
    
    @property
    def connect_db(self):
        self.db = Database(name='admin')

    async def list_accounts(self):
        query = """SELECT * FROM suppliers-accounts"""
        await self.db.async_connection.connect()
        results = await self.db.async_connection.fetch_all(query=query)
        await self.db.async_connection.disconnect()
        self.accounts_list:list = []
        self.accounts_index:list = []
        for item in results:
            self.accounts_list.append({
                "id": item[1],                
                "data": json.loads(item[2]),    
                "transactions": json.loads(item[3])               
            })
            self.accounts_index.append(
                {
                    "id": item[1],
                    "data": item[2]                                  
                }
            )       
        return self.accounts_index

    @property
    def save(self):        
        self.db.session.add(self)
        self.db.session.commit()    

def createAdmins():
    cnf._make_dir(cnf.DATABASE_DIR)
    db = Database(name='admin')    
    db.create_admin_table
    
def createTools():
    cnf._make_dir(cnf.DATABASE_DIR)
    db = Database(name='tools')
    db.create_tools_table
    
def setup():
    createAdmins()
    time.sleep(1)
    createTools()

#setup()