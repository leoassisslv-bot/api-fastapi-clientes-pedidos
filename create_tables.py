from app.db import get_connection

conn = get_connection()
cursor = conn.cursor()

# =========================
# TABELA CLIENTES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(30),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# TABELA PEDIDOS
# =========================

cursor.execute("""
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

# =========================
# GARANTE COLUNAS NOVAS
# =========================

cursor.execute("""
ALTER TABLE clientes
ADD COLUMN IF NOT EXISTS telefone VARCHAR(30)
""")

cursor.execute("""
ALTER TABLE clientes
ADD COLUMN IF NOT EXISTS criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
""")

cursor.execute("""
ALTER TABLE pedidos
ADD COLUMN IF NOT EXISTS profissional VARCHAR(100)
""")

cursor.execute("""
ALTER TABLE pedidos
ADD COLUMN IF NOT EXISTS data_servico TIMESTAMP
""")

cursor.execute("""
ALTER TABLE pedidos
ADD COLUMN IF NOT EXISTS criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
""")

conn.commit()

cursor.close()
conn.close()

print("Tabelas atualizadas com sucesso!")