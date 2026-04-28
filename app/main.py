from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db import get_connection

app = FastAPI()

class ClienteCreate(BaseModel):
    nome: str
    email: str
    idade: int

@app.get("/")
def root():
    return {"mensagem": "API funcionando"}

@app.get("/clientes")
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

@app.get("/clientes/{cliente_id}")
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

@app.put("/clientes/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente: ClienteCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:

            # verifica se existe
            cur.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
            existe = cur.fetchone()

            if not existe:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")

            # atualiza
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

@app.delete("/clientes/{cliente_id}")
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


@app.post("/clientes")
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


class PedidoCreate(BaseModel):
    cliente_id: int
    produto: str
    valor: float


@app.post("/pedidos")
def criar_pedido(pedido: PedidoCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:

            # verifica se cliente existe
            cur.execute("SELECT id FROM clientes WHERE id = %s", (pedido.cliente_id,))
            cliente = cur.fetchone()

            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")

            # insere pedido
            cur.execute("""
                INSERT INTO pedidos (cliente_id, produto, valor)
                VALUES (%s, %s, %s)
                RETURNING id, cliente_id, produto, valor, criado_em
            """, (pedido.cliente_id, pedido.produto, pedido.valor))

            novo = cur.fetchone()
            conn.commit()

    return {
        "id": novo[0],
        "cliente_id": novo[1],
        "produto": novo[2],
        "valor": float(novo[3]),
        "criado_em": str(novo[4])
    }
    
@app.get("/pedidos")
def listar_pedidos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    pedidos.id,
                    clientes.nome,
                    pedidos.produto,
                    pedidos.valor,
                    pedidos.criado_em
                FROM pedidos
                JOIN clientes ON pedidos.cliente_id = clientes.id
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
            "criado_em": str(linha[4]),
        })

    return pedidos


@app.get("/clientes/{cliente_id}/pedidos")
def listar_pedidos_do_cliente(cliente_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
            cliente = cur.fetchone()

            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")

            cur.execute("""
                SELECT
                    pedidos.id,
                    pedidos.produto,
                    pedidos.valor,
                    pedidos.criado_em
                FROM pedidos
                WHERE pedidos.cliente_id = %s
                ORDER BY pedidos.id
            """, (cliente_id,))
            dados = cur.fetchall()

    pedidos = []

    for linha in dados:
        pedidos.append({
            "id": linha[0],
            "produto": linha[1],
            "valor": float(linha[2]),
            "criado_em": str(linha[3]),
        })

    return pedidos