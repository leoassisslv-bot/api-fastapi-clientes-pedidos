from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import get_connection


router = APIRouter()


class UsuarioCreate(BaseModel):
    nome_empresa: str
    email: str
    senha: str


@router.post("/api/usuarios")
def criar_usuario(dados: UsuarioCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT id FROM usuarios
                WHERE email = %s
            """, (dados.email,))

            usuario_existente = cur.fetchone()

            if usuario_existente:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe um usuário com este email."
                )

            cur.execute("""
                INSERT INTO usuarios (nome_empresa, email, senha)
                VALUES (%s, %s, %s)
                RETURNING id, nome_empresa, email
            """, (
                dados.nome_empresa,
                dados.email,
                dados.senha
            ))

            novo_usuario = cur.fetchone()

        conn.commit()

    return {
        "mensagem": "Usuário criado com sucesso.",
        "usuario": {
            "id": novo_usuario[0],
            "nome_empresa": novo_usuario[1],
            "email": novo_usuario[2]
        }
    }