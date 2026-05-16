import os
from dotenv import load_dotenv
import psycopg

# Carrega variáveis do .env
load_dotenv()


# =========================
# CONEXÃO COM POSTGRESQL
# =========================
# Responsável por conectar no banco local ou Render

def get_connection():

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# =========================
# CRIAÇÃO / ATUALIZAÇÃO
# DAS TABELAS
# =========================

def criar_tabelas():

    with get_connection() as conn:

        with conn.cursor() as cur:

            # =========================
            # TABELA CLIENTES
            # =========================

            cur.execute("""
                CREATE TABLE IF NOT EXISTS clientes (

                    id SERIAL PRIMARY KEY,

                    nome VARCHAR(100),

                    email VARCHAR(100),

                    telefone VARCHAR(30),

                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # =========================
            # TABELA SERVIÇOS (PEDIDOS)
            # =========================

            cur.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (

                    id SERIAL PRIMARY KEY,

                    cliente_id INTEGER REFERENCES clientes(id),

                    produto VARCHAR(100),

                    valor NUMERIC(10,2),

                    profissional VARCHAR(100),

                    data_servico TIMESTAMP,

                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Adiciona coluna profissional caso não exista
        cur.execute("""
                    ALTER TABLE pedidos
                   ADD COLUMN IF NOT EXISTS profissional VARCHAR(100)
             """)

              # Adiciona coluna data_servico caso não exista
        cur.execute("""
                     ALTER TABLE pedidos
                   ADD COLUMN IF NOT EXISTS data_servico TIMESTAMP
           """)

            # =========================
            # GARANTE NOVAS COLUNAS
            # MESMO EM BANCOS ANTIGOS
            # =========================

            # CLIENTES

            cur.execute("""
                ALTER TABLE clientes
                ADD COLUMN IF NOT EXISTS telefone VARCHAR(30)
            """)

            # PEDIDOS

            cur.execute("""
                ALTER TABLE pedidos
                ADD COLUMN IF NOT EXISTS profissional VARCHAR(100)
            """)

            cur.execute("""
                ALTER TABLE pedidos
                ADD COLUMN IF NOT EXISTS data_servico TIMESTAMP
            """)

            cur.execute("""
                ALTER TABLE pedidos
                ADD COLUMN IF NOT EXISTS criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)

            # Salva alterações
            conn.commit()

    print("Banco atualizado com sucesso!")