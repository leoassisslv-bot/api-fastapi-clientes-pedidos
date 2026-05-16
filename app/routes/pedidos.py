from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import get_connection


# =========================
# CONFIGURAÇÃO DAS ROTAS
# =========================

router = APIRouter()


# =========================
# MODELO DE SERVIÇO
# =========================
# Apesar do arquivo ainda se chamar pedidos.py,
# aqui ele representa os serviços cadastrados no sistema.

class PedidoCreate(BaseModel):

    cliente_id: int
    produto: str
    valor: float
    profissional: str
    data_servico: str


# =========================
# CRIAR SERVIÇO
# =========================
# Cadastra um serviço vinculado a um cliente existente.

@router.post("/pedidos")
def criar_pedido(pedido: PedidoCreate):

    with get_connection() as conn:

        with conn.cursor() as cur:

            # Verifica se o cliente existe antes de cadastrar o serviço.
            cur.execute(
                "SELECT id FROM clientes WHERE id = %s",
                (pedido.cliente_id,)
            )

            cliente = cur.fetchone()

            if not cliente:

                raise HTTPException(
                    status_code=404,
                    detail="Cliente não encontrado"
                )

            cur.execute("""
                INSERT INTO pedidos (
                    cliente_id,
                    produto,
                    valor,
                    profissional,
                    data_servico
                )

                VALUES (%s, %s, %s, %s, %s)

                RETURNING
                    id,
                    cliente_id,
                    produto,
                    valor,
                    profissional,
                    data_servico,
                    criado_em
            """, (
                pedido.cliente_id,
                pedido.produto,
                pedido.valor,
                pedido.profissional,
                pedido.data_servico
            ))

            novo = cur.fetchone()

            conn.commit()

    return {
        "id": novo[0],
        "cliente_id": novo[1],
        "produto": novo[2],
        "valor": float(novo[3]),
        "profissional": novo[4],
        "data_servico": str(novo[5]),
        "criado_em": str(novo[6])
    }


# =========================
# LISTAR SERVIÇOS
# =========================
# Retorna todos os serviços com o nome do cliente.
# Essa rota alimenta a lista de serviços e a agenda no frontend.

@router.get("/pedidos")
def listar_pedidos():

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    pedidos.id,
                    clientes.nome,
                    pedidos.produto,
                    pedidos.valor,
                    pedidos.profissional,
                    pedidos.data_servico,
                    pedidos.criado_em

                FROM pedidos

                JOIN clientes
                    ON pedidos.cliente_id = clientes.id

                ORDER BY pedidos.id
            """)

            dados = cur.fetchall()

    pedidos = []

    for linha in dados:

        pedidos.append({
            "id": linha[0],
            "cliente": linha[1],
            "produto": linha[2],
            "valor": float(linha[3]),
            "profissional": linha[4],
            "data_servico": str(linha[5]),
            "criado_em": str(linha[6]),
        })

    return pedidos


# =========================
# LISTAR SERVIÇOS DE UM CLIENTE
# =========================
# Retorna apenas os serviços vinculados a um cliente específico.

@router.get("/clientes/{cliente_id}/pedidos")
def listar_pedidos_do_cliente(cliente_id: int):

    with get_connection() as conn:

        with conn.cursor() as cur:

            # Confirma se o cliente existe.
            cur.execute(
                "SELECT id FROM clientes WHERE id = %s",
                (cliente_id,)
            )

            cliente = cur.fetchone()

            if not cliente:

                raise HTTPException(
                    status_code=404,
                    detail="Cliente não encontrado"
                )

            cur.execute("""
                SELECT
                    id,
                    produto,
                    valor,
                    profissional,
                    data_servico,
                    criado_em

                FROM pedidos

                WHERE cliente_id = %s

                ORDER BY id
            """, (cliente_id,))

            dados = cur.fetchall()

    pedidos = []

    for linha in dados:

        pedidos.append({
            "id": linha[0],
            "produto": linha[1],
            "valor": float(linha[2]),
            "profissional": linha[3],
            "data_servico": str(linha[4]),
            "criado_em": str(linha[5]),
        })

    return pedidos


# =========================
# DELETAR SERVIÇO
# =========================
# Remove um serviço pelo ID.

@router.delete("/pedidos/{pedido_id}")
def deletar_pedido(pedido_id: int):

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                "SELECT id FROM pedidos WHERE id = %s",
                (pedido_id,)
            )

            existe = cur.fetchone()

            if not existe:

                raise HTTPException(
                    status_code=404,
                    detail="Serviço não encontrado"
                )

            cur.execute(
                "DELETE FROM pedidos WHERE id = %s",
                (pedido_id,)
            )

            conn.commit()

    return {
        "mensagem": "Serviço deletado com sucesso"
    }