from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import get_connection


router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/api/login")
def login(dados: LoginRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome_empresa, email
                FROM usuarios
                WHERE email = %s AND senha = %s
            """, (
                dados.email,
                dados.senha
            ))

            usuario = cur.fetchone()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )

    return {
        "mensagem": "Login realizado com sucesso.",
        "usuario": {
            "id": usuario[0],
            "nome_empresa": usuario[1],
            "email": usuario[2]
        }
    }