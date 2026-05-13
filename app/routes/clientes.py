from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import get_connection

router = APIRouter()


class ClienteCreate(BaseModel):
    nome: str
    email: str
    idade: int


@router.get("/clientes")
def listar_clientes():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome, email, idade, criado_em
                FROM clientes
                ORDER BY id
            """)
            dados = cur.fetchall()

    clientes = []

    for linha in dados:
        clientes.append({
            "id": linha[0],
            "nome": linha[1],
            "email": linha[2],
            "idade": linha[3],
            "criado_em": str(linha[4]),
        })

    return clientes


@router.get("/clientes/{cliente_id}")
def buscar_cliente_por_id(cliente_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome, email, idade, criado_em
                FROM clientes
                WHERE id = %s
            """, (cliente_id,))
            cliente = cur.fetchone()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return {
        "id": cliente[0],
        "nome": cliente[1],
        "email": cliente[2],
        "idade": cliente[3],
        "criado_em": str(cliente[4]),
    }


@router.post("/clientes")
def criar_cliente(cliente: ClienteCreate):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO clientes (nome, email, idade)
                    VALUES (%s, %s, %s)
                    RETURNING id, nome, email, idade, criado_em
                """, (cliente.nome, cliente.email, cliente.idade))

                novo_cliente = cur.fetchone()
                conn.commit()

        return {
            "id": novo_cliente[0],
            "nome": novo_cliente[1],
            "email": novo_cliente[2],
            "idade": novo_cliente[3],
            "criado_em": str(novo_cliente[4]),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")


@router.put("/clientes/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente: ClienteCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
            existe = cur.fetchone()

            if not existe:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")

            cur.execute("""
                UPDATE clientes
                SET nome = %s, email = %s, idade = %s
                WHERE id = %s
                RETURNING id, nome, email, idade, criado_em
            """, (cliente.nome, cliente.email, cliente.idade, cliente_id))

            cliente_atualizado = cur.fetchone()
            conn.commit()

    return {
        "id": cliente_atualizado[0],
        "nome": cliente_atualizado[1],
        "email": cliente_atualizado[2],
        "idade": cliente_atualizado[3],
        "criado_em": str(cliente_atualizado[4]),
    }


@router.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
            existe = cur.fetchone()

            if not existe:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")

            cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conn.commit()

    return {"mensagem": "Cliente deletado com sucesso"}