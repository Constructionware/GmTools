from aspire.core.security_service import CORSMiddleware
from aspire.core.reactor import (
    Jinja2Templates,
    JSONResponse,
    Route,
    Mount,
    StaticFiles
)
from aspire.core.app_stack import Aspiration

from Server.models import cnf

templates = Jinja2Templates(directory=cnf.APP_TEMPLATES)

async def appServer(request):
    return templates.TemplateResponse('index.html', {'request': request})

async def catchRoute(request):
    return templates.TemplateResponse('index.html', {'request': request})

async def webManifest(request):
    return templates.TemplateResponse('manifest.json', {'request': request})

routes =[
    Route('/', endpoint=appServer),    
    Route('/manifest.json', endpoint=webManifest),
    Route('/{path}', endpoint=catchRoute),
    Mount('/static', StaticFiles(directory=cnf.APP_STATIC))


]

retool_ui = Aspiration(
    routes=routes,
    debug=cnf.DEBUG
)

retool_ui.add_middleware(
    CORSMiddleware,
    allow_origins=cnf.ORIGINS,
    allow_methods=cnf.METHODS,
    allow_headers=cnf.HEADERS,
    allow_credentials=cnf.CREDENTIALS,
    allow_origin_regex=cnf.ORIGIN_REGEX,
    expose_headers=cnf.EXPOSED_HEADERS,
    max_age=cnf.MAX_AGE
)