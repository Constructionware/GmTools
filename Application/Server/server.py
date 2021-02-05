
from aspire.core.security_service import CORSMiddleware
from aspire import API

from Server.config import config

cnf = config.get('dev_con')

from Server.models import Tool

gmTools = API(
    debug=cnf.DEBUG,
    title=cnf.TITLE,
    version=cnf.VERSION,
    description=cnf.DESCRIPTION,
    terms_of_service=cnf.TERMS,
    contact=cnf.CONTACT,
    license=cnf.LICENSE,
    auto_escape=cnf.AUTO_ESCAPE,
    #templates_dir=cnf.TEMPLATES_DIR,
    #static_dir=cnf.STATIC_DIR,
    secret_key=cnf.SECRET_KEY,
    #static_route=cnf.STATIC_ROUTE,
    #docs_route=cnf.DOCUMENT_ROUTE
)

gmTools.add_middleware(
    CORSMiddleware,
    allow_origins=cnf.ORIGINS,
    allow_methods=cnf.METHODS,
    allow_headers=cnf.HEADERS,
    allow_credentials=cnf.CREDENTIALS,
    allow_origin_regex=cnf.ORIGIN_REGEX,
    expose_headers=cnf.EXPOSED_HEADERS
)

#------ ROUTES MOUNT POINTS --------

@gmTools.route('/')
async def index(req, resp):   
    data = {"product": cnf.TITLE, "description": cnf.DESCRIPTION}
    tool = Tool("Laser Measure")
    tool.tool_type = "GLM42"
    tool.brand="bosch"
    tool.category = 'Measurement'
    tool.specification["power"]["source"] = "2xAAA Battery"
    tool.specification["power"]["volts"] = 3
    tool.specification["power"]["current"] = 0.3
    tool.specification["props"] = ["real time", "five measurement mode"] 
    tool.specification["range"] = "135 ft"
    tool.available = True
    tool.condition = ["New"]
    tool.url = f"{tool.url}/{tool.id}"
    tool.cost["jad"] = 15000.00
    

    data["tool"] = {
        "id": tool.id,
        "name": tool.name,
        "brand": tool.brand,
        "type": tool.tool_type,
        "category": tool.category,
        "specifications": tool.specification,
        "available": tool.available,
        "condition": tool.condition,
        "cost": tool.cost,
        "url": tool.url,
        "images": tool.images_url


    }

    resp.media = data


#------ WEBSOCKET MOUNT POINTS -----


#------ API MOUNT POINTS -----------

#------ MAIL PROTOCOL MOUNT POINT --

#------- CLIENT APPLICATIONS MOUNT POINTS ---

