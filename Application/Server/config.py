import logging
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
    #---  SECURITY -----

    SECRET_KEY:str = None
    AUTO_ESCAPE:bool = False

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

    #---- RUNTIME ------
    MODE:str = 'Default'
    DEBUG:bool = True
    LOOP:str = 'asyncio'
    ACCESS_LOG:bool = False

    #---- INTITIALIZE -----

    def __init__(self):
        self.setup()

    def setup(self):
        self.keygen = GenerateId()
        self.SECRET_KEY = self.keygen.gen_id('app')

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