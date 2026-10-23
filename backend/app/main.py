from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, select
from typing import Optional
from datetime import datetime
import uuid

# Importações dos nossos módulos locais
from app.database import criar_tabelas, get_session
from app.logging_config import configurar_logs
import structlog

# 1. Configura os logs em JSON
configurar_logs()
logger = structlog.get_logger()

class OrdemServico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    categoria: str = "Geral"
    status: str = "aberta"
    criada_em: datetime = Field(default_factory=datetime.utcnow)

@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield

app = FastAPI(lifespan=lifespan, title="Manutenção por Voz")

# 2. CONFIGURAÇÃO DE CORS (A correção do erro no Edge)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite o frontend localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. MIDDLEWARE DE LOGS (Gera um ID único para cada requisição)
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    corr_id = str(uuid.uuid4())
    # Vincula o ID ao contexto do log
    with structlog.contextvars.bound_contextvars(correlation_id=corr_id):
        logger.info("request_started", method=request.method, path=request.url.path)
        response = await call_next(request)
        logger.info("request_finished", status_code=response.status_code)
        return response

@app.post("/os", response_model=OrdemServico)
def criar_os(descricao: str, session: Session = Depends(get_session)):
    categoria = "Geral"
    texto = descricao.lower()
    if "vibra" in texto or "rolamento" in texto:
        categoria = "Mecânica"
    elif "aqueci" in texto or "elétric" in texto or "fio" in texto:
        categoria = "Elétrica"

    os = OrdemServico(descricao=descricao, categoria=categoria)
    session.add(os)
    session.commit()
    session.refresh(os)
    
    # Log específico da regra de negócio
    logger.info("os_criada", os_id=os.id, categoria=os.categoria)
    
    return os

@app.get("/os")
def listar_os(session: Session = Depends(get_session)):
    return session.exec(select(OrdemServico)).all()