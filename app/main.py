from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.db import criar_tabelas
from app.routes.clientes import router as clientes_router
from app.routes.pedidos import router as pedidos_router


# Criação principal da aplicação FastAPI
app = FastAPI(
    title="NextStudio",
    description="Sistema SaaS simples para gestão de clientes, serviços e agenda.",
    version="1.0.0"
)

# Configuração dos arquivos estáticos: CSS, JS, imagens etc.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configuração da pasta onde ficam os templates HTML
templates = Jinja2Templates(directory="app/templates")

# Registro das rotas da aplicação
app.include_router(clientes_router)
app.include_router(pedidos_router)


@app.on_event("startup")
def iniciar_banco():
    """
    Executa automaticamente quando a aplicação inicia.

    Essa função garante que as tabelas e colunas necessárias existam
    tanto no banco local quanto no banco online do Render.
    """
    criar_tabelas()


@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    """
    Tela inicial de login.
    """

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """
    Painel administrativo do sistema.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )