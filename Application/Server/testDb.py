import asyncio
import os, sqlalchemy as sql
from databases import Database

#metadata = sql.MetaData()
"""
notes = sql.Table(
    "category",
    sql.Column("id", sql.Integer, primary_key=True),
    sql.Column("name", sql.String(length=100))
)
"""

DATABASE_DIR:str = os.path.realpath("D:/ToolDB")
dbh = os.path.join(DATABASE_DIR, 'gmt-toos.sqlite')
print(dbh)
db = Database(f"sqlite:///{dbh}")

async def db_process():
    #query = '''CREATE TABLE category (id INTEGER PRIMARY KEY, name VARCHAR(100))'''
    await db.connect()
    #await db.execute(query=query)
    #query = """INSERT INTO category(name) VALUES(:name)"""
    #values = [{"name": "Drills"},{"name": "Jack Hammers"},{"name": "Saws"},{"name": "Chargers"},{"name": "Band Saws"},]
    #await db.execute_many(query=query, values=values)
    query = '''SELECT * FROM category'''
    rows = await db.fetch_all(query=query)    
    await db.disconnect()
    print('Categories', rows)


asyncio.run(db_process())