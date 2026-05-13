from app.routes.pedidos import router as pedidos_router
from app.routes.clientes import router as clientes_router
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db import get_connection
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(clientes_router)
app.include_router(pedidos_router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

    
