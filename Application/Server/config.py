import logging
import os
from aspire.core.reactor import Request
from aspire.core.security_service import GenerateId

class Config:
    #----- ABOUT APPLICATION --------
    TITLE:str = "GM Tools and Electronics"
    DESCRIPTION:str = "GM Tools. Your Premier Supplier of New and Refurbished Construction Tools and Electronics"
    TERMS:str = "https://github.com/Constructionware/GmTools/terms"
    CONTACT:dict = {
        "name": "GMTools Support Team",
        "url": "https://gmtools.com/support",
        "email": "support@gmtools.com"
    }
    LICENSE:dict = {
        "name": "MIT",
        "url": "opensource.org/license/MIT"
    }
    VERSION:float = 1.0
    #--- APPLICATION DIRECTORIES -----
    BASE_DIR:str = os.path.dirname(os.path.realpath(__file__))
    DATABASE_DIR:str = os.path.realpath("D:/ToolDB")
    STATIC_DIR:str =  os.path.realpath("D:/ReTool")   
    IMAGES_DIR = os.path.join(STATIC_DIR, 'Images')
    BATTERY_TOOLS = os.path.join(IMAGES_DIR, 'Batterytools')
    FUEL_TOOLS = os.path.join(IMAGES_DIR, 'Fueltools')
    POWER_TOOLS = os.path.join(IMAGES_DIR, 'Powertools')
    TEMPLATES_DIR = os.path.join(BASE_DIR[:32], 'Ui')
    APP_TEMPLATES = os.path.join(TEMPLATES_DIR, 'retool')
    APP_STATIC = os.path.join(APP_TEMPLATES, 'static')

    #---  SECURITY -----

    AUTO_ESCAPE:bool = False
    SECRET_KEY:str = None
    SERVE_HTTPS:bool = False
    SSL_REDIRECT =False
    
    #--- NETWORK ------
  
    PORT:int = 7707
    HOST:str = '0.0.0.0'
    CONNECTIONS:int = 1000
    MAX_REQUESTS:int = 100
    ORIGINS:list = ["*"]
    METHODS:list = ["*"]
    HEADERS:list = ["*"]
    CREDENTIALS:bool = False
    ORIGIN_REGEX:object = None
    EXPOSED_HEADERS:list = [
        "Access-Controll-Allow-Origin",
        "Access-Controll-Allow-Credentials",
        "Access-Controll-Allow-Expose-Headers"
    ]
    MAX_AGE:int = 3600

    #---- DATABASE ------

    SQL_DATABASE_URI:dict = {
        "tools": f"sqlite:///{DATABASE_DIR}/gmt-toos.sqlite",
        "admin": f"sqlite:///{DATABASE_DIR}/gmt-admin.sqlite"
    }

    #------ ROUTES -----
    STATIC_ROUTE:str = '/static'
    DOCUMENT_ROUTE:str = '/docs'

    
    #---- RUNTIME ------

    MODE:str = 'Default'
    DEBUG:bool = True
    LOOP:str = 'asyncio'
    ACCESS_LOG:bool = False

    #---- INTITIALIZE -----

    def __init__(self):
        self.__setup     

    @property
    def _set_keygenerator(self):
        self.keygen = GenerateId()
        self.SECRET_KEY = self.keygen.gen_id('app')

    
    def _make_dir(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        pass


    def _list_directory(self, directory):
        # return list of directories
        return os.listdir( directory )

    @property
    def _create_directories(self):
        ''' Create System Directories '''   
        self.dirs = [
            self.DATABASE_DIR, 
            self.STATIC_DIR,
            self.IMAGES_DIR,
            self.BATTERY_TOOLS,
            self.FUEL_TOOLS,
            self.POWER_TOOLS
        ]
        for item in self.dirs:
            self._make_dir(item)

    @property
    def __setup(self):
        self._set_keygenerator
        self._create_directories

    def __repr__(self):
        return f"{self.TITLE} {self.MODE} Configuration Object."



class DevelopmentConfig(Config):
    #--- NETWORK ------
    
    #---- RUNTIME ------
    MODE:str = 'Development'
    DEBUG:bool = True



class TestConfig(Config):   
    #--- NETWORK ------
    HOST:str = '127.0.0.1'
    
    #---- RUNTIME ------
    MODE:str = 'Test'
    DEBUG:bool = False



class ProductionConfig(Config):   
    #---  SECURITY -----

    AUTO_ESCAPE:bool = True 
    #--- NETWORK ------
    CONNECTIONS:int = 10000
    MAX_REQUESTS:int = 1000

    #---- RUNTIME ------
    MODE:str = 'Production'
    DEBUG:bool = False



config = dict(
    def_con = Config(),
    dev_con = DevelopmentConfig(),
    tes_con = TestConfig(),
    pro_con = ProductionConfig(),

)
