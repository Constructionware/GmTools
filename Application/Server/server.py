
from aspire.core.security_service import CORSMiddleware
from aspire import API

from Server.config import config


cnf = config.get('dev_con')


from Server.models import PowerTool
from Server.api import toolsApi
from Server.uiServer import retool_ui

gmTools = API(
    debug=cnf.DEBUG,
    title=cnf.TITLE,
    version=cnf.VERSION,
    description=cnf.DESCRIPTION,
    terms_of_service=cnf.TERMS,
    contact=cnf.CONTACT,
    license=cnf.LICENSE,
    auto_escape=cnf.AUTO_ESCAPE,
    templates_dir=cnf.APP_TEMPLATES,
    static_dir=cnf.APP_STATIC,
    secret_key=cnf.SECRET_KEY,
    enable_https=cnf.SERVE_HTTPS,
    static_route=cnf.STATIC_ROUTE,
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

gmTools.mount('/retool', retool_ui)
#------ WEBSOCKET MOUNT POINTS -----


#------ API MOUNT POINTS -----------
gmTools.mount('/tools', toolsApi)
#------ MAIL PROTOCOL MOUNT POINT --

#------- CLIENT APPLICATIONS MOUNT POINTS ---

