#api.py
import time
import json
import os
from PIL import Image
from os import getlogin, name
from aspire.core.app_stack import Aspiration
from aspire.core.reactor import ( JS, JSONResponse, PlainTextResponse, FileResponse, StaticFiles, Route, Mount)
from aspire.core.security_service import requires, Request

from Server.models import cnf
from Server.models import ( Category, BatteryTool, FuelTool, PowerTool )
from Server.models import ( Supplier, Client, SalesAgent )
from Server.models import ( Account, Supply, Sale )


#----------- Utitities -------------

def select_tool(tool_type:str=None, tool_name:str=None):
    ''' Selects a Tool Object bassed on tool type. eg: power, battery, fuel'''
    selector = {
        "battery": BatteryTool(tool_name),
        "fuel": FuelTool(tool_name),
        "power": PowerTool(tool_name)
    }
    return selector.get(tool_type, None)

def load_tool_library():
    battery_tool = BatteryTool()
    fuel_tool = FuelTool()
    power_tool = PowerTool()

def image_dir(tool_type:str=None):
    if tool_type:
        select_dir = {
            "battery": cnf.BATTERY_TOOLS,
            "fuel": cnf.FUEL_TOOLS,
            "power": cnf.POWER_TOOLS
        }
        return select_dir.get(tool_type, None)
    return None

def upload_url(tool_type:str=None):
    
    if tool_type:
        select_url = {
            "battery": f"/tools/static/images/Batterytools/",
            "fuel": f"/tools/static/images/Fueltools/",
            "power": f"/tools/static/images/Powertools/"
        }
        return select_url.get(tool_type, None)
    return None

#------------ Api Routes ---------------
 
async def index(request):
    tools = []
    battery_tool = BatteryTool()
    fuel_tool = FuelTool()
    power_tool = PowerTool()
    battery_tool = await battery_tool.list_tools()
    fuel_tool = await fuel_tool.list_tools()
    power_tool = await power_tool.list_tools()
    tools.extend(battery_tool)
    tools.extend(fuel_tool)
    tools.extend(power_tool)
    return JSONResponse({
        "protocol": "GMTools Api",
        "server": cnf.DESCRIPTION,        
        "tools": tools
    })

async def inventory(request):
    tools = []
    battery_tool = BatteryTool()
    fuel_tool = FuelTool()
    power_tool = PowerTool()
    await battery_tool.list_tools()
    await fuel_tool.list_tools()
    await power_tool.list_tools()    
    tools.extend(battery_tool.inventory)
    tools.extend(fuel_tool.inventory)
    tools.extend(power_tool.inventory)
    return JSONResponse({
        "protocol": "GMTools Api",
        "server": cnf.DESCRIPTION,        
        "tools": tools
    })

async def upload_tool_image(request):
    ''' Accepts parameters tool_type'''
    #data = await request.json()
    tool_type = request.path_params['tool_type']   
    form = await request.form()
    filename = form["image"].filename
    model = form["model"]
    # Construct Url
    img_home = image_dir(tool_type=tool_type)
    url = os.path.join(img_home, filename) 
    contents = await form["image"].read()   
    with open(url, 'wb') as f:
        f.write(contents)
    f.close                                
    #--- Optimize -----
    img = Image.open(url) 
    if img.width > 180:

        new_img = img.resize((180, 148))
        newfile_name = f"{model}-{filename}"
        new_url = os.path.join(img_home, newfile_name) 
        new_img.save(new_url)
        new_img.close()        
        img.close()
        os.remove(url)    
        return JSONResponse({
            "success": True,
            "type": tool_type,
            "uploaded_file": newfile_name,
            "image_url": upload_url(tool_type=tool_type)

            })
    img.close()
    return JSONResponse({
            "success": True,
            "type": tool_type,
            "uploaded_file": filename,
            "image_url": upload_url(tool_type=tool_type)         

            })
    

async def create_tool(request):    
    tool_type = request.path_params['tooltype']
    if request.method == 'GET':
        return JSONResponse({
            "data": request.method,
            "type": tool_type
            })
    data = await request.json()
    tool = select_tool(tool_type=tool_type, tool_name=data['name'])
    tool.brand = data['brand']
    tool.type = tool_type
    tool.specification = data['specification']
    tool.data = data['data']
    tool.price = data['price']
    tool.data['created_by'] = getlogin()
    tool.save
    return JSONResponse({
            "id": tool.tool_id,
            "name": tool.name,
            "brand": tool.brand,
            "type": tool.type,
            "specification": tool.specification,
            "data": tool.data,
            "price": tool.price
            })

#------------ Tool Categories ------------------
async def create_category(request):
    name=request.path_params['category']    
    category = Category()
    category.name = name
    try:
        category.save
        message = {"success": True, "message": f'Category {name} Created.'}
    except Exception as e:
        message = {"success": False, "message": f'Category {name} Already Exists.'}

    #await category.list_category()
    return JSONResponse(message)

async def categories(request):
    cat = Category()
    cat_list = await cat.list_category()
    items:list = []
    for item in cat_list:
        items.append(item[1])
    return JSONResponse(items)

#----------- Purchasers -----------------------

async def create_purchaser(request):
    name=request.path_params['name'].split('-') 
    if request.method == 'GET':         
        if len(name) > 1:
            # User sends get firstname-lastname request
            client = Client(firstname=name[0], lastname=name[1], directive='search')
        else:
            # User sends get client_id request
            client = Client(client_id=name[0] ) 
            data = client.get
            return JSONResponse({
                "data": data[0]
            })

        return JSONResponse({
            "request_data": {
                "method": request.method,
                "time": time.ctime()
            },
            "purchaser": f"{client.firstname} {client.lastname}",
            "id": client.client_id,
            "data": data
            })
    # Request to create a new purchaser
    data = await request.json()
    client = Client(firstname=name[0], lastname=name[1], directive='new')        
    client.data = data['data']
    client.data['created_by'] = getlogin()
    try:
        client.save
        message = {"success": True, "message": f'Client {name} Created.'}
        return JSONResponse({
            "request_data": {
                "message": message,
                "method": request.method,
                "time": time.ctime()
            },
            "purchaser": f"{client.firstname} {client.lastname}",
            "id": client.client_id,
            "data": client.data
            })
    
    except Exception as e:
        message = {"success": False, "message": f'Client {name} Already Exists.'}
        return JSONResponse({
            "request_data": {
                "message": message,
                "method": request.method,
                "time": time.ctime()
            }
        })
 
async def purchasers(request):
    buyer = Client()
    buyers = await buyer.list_purchasers
    return JSONResponse(buyers)



# Retreive a single tool data given it's tool_id
def get_tool(request):
    tool_id = request.path_params['id']
    #power_tool = PowerTool.query.filter_by(tool_id=tool_id).first()
    #print(power_tool)
    tool = {
        'id': tool_id
    }
    return JSONResponse(tool)

# ---- RUNTIME -------

async def startup(request):
    return JSONResponse({'message': 'Api started'})

async def shutdown(request):
    return JSONResponse({'message': 'Shutting Down'})

routes = [
    Route('/', index),
    Route('/inventory', inventory, methods=['GET']),
    Route('/create/{tooltype}', create_tool, methods=['GET', 'POST']),
    Route('/get/{id}', get_tool, methods=['GET']),
    Route('/category', categories, methods=['GET']),
    Route('/newcategory/{category}', create_category, methods=['GET']),
    Route('/buyer', purchasers, methods=['GET'] ),
    Route('/buyer/{name}', create_purchaser, methods=['GET', 'POST', 'PUT', 'DELETE'] ),
    Route('/upload/{tool_type}', upload_tool_image, methods=['POST']),
    Mount('/static', StaticFiles(directory=cnf.STATIC_DIR))
]

toolsApi = Aspiration(
    debug=True, 
    routes=routes,
    on_startup=[startup],
    on_shutdown=[shutdown] 
)