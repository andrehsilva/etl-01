import pandas as pd
import random
from datetime import datetime, timedelta

# Gerar 100 clientes
nomes = ['João', 'Maria', 'Pedro', 'Ana', 'Carlos', 'Lucas', 'Mariana', 'Fernanda', 'Bruno', 'Juliana',
         'Paulo', 'Camila', 'Eduardo', 'Larissa', 'Mateus', 'Patrícia', 'Thiago', 'Renata', 'Felipe', 'Aline',
         'Ricardo', 'Beatriz', 'Gustavo', 'Tatiane', 'Danilo', 'Sabrina', 'Leandro', 'Natália', 'André', 'Débora',
         'Vinícius', 'Viviane', 'Gabriel', 'Isabela', 'Fábio', 'Jéssica', 'Roberto', 'Amanda', 'Marcelo', 'Lívia']
sobrenomes = ['Silva', 'Souza', 'Oliveira', 'Pereira', 'Costa', 'Rodrigues', 'Almeida', 'Nascimento', 'Lima', 'Gomes']

clientes = []
for i in range(1, 101):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = nome.lower().replace(" ", ".") + "@gmail.com"
    clientes.append((i, nome, email))

df_clientes = pd.DataFrame(clientes, columns=["ClienteId", "Nome", "Email"])

# Gerar 100 pedidos
pedidos = []
for i in range(1, 101):
    cliente_id = random.randint(1, 100)
    data = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 450))
    pedidos.append((i, cliente_id, data.date()))

df_pedidos = pd.DataFrame(pedidos, columns=["PedidoId", "ClienteId", "Data"])

# Itens fixos
itens = [
    ('i1', 'Arroz'),
    ('i2', 'Feijão'),
    ('i3', 'Carne'),
    ('i4', 'Salada'),
    ('i5', 'Batata'),
    ('i6', 'Pão'),
    ('i7', 'Queijo'),
    ('i8', 'Leite'),
    ('i9', 'Ovo'),
    ('i10', 'Banana')
]
df_itens = pd.DataFrame(itens, columns=["Id", "Nome"])

# Gerar 100 linhas de pedido
linhas_pedido = []
pedido_ids = [p[0] for p in pedidos]
line_number = {}

for _ in range(100):
    pedido_id = random.choice(pedido_ids)
    line_number[pedido_id] = line_number.get(pedido_id, 0) + 1
    line = line_number[pedido_id]
    item = random.choice(itens)
    quantidade = random.randint(1, 15)
    preco_unitario = random.choice([5.00, 8.50, 10.00, 12.00])
    valor_total = round(quantidade * preco_unitario, 2)
    linhas_pedido.append((pedido_id, line, item[0], quantidade, preco_unitario, valor_total))

df_linhas = pd.DataFrame(linhas_pedido, columns=["PedidoId", "Line", "ItemId", "Quantidade", "PrecoUnitario", "ValorTotal"])

# Salvar em arquivos CSV
path_clientes = "output/clientes.csv"
path_pedidos = "output/pedidos.csv"
path_itens = "output/itens.csv"
path_linhas = "output/linhas_pedido.csv"

df_clientes.to_csv(path_clientes, index=False)
df_pedidos.to_csv(path_pedidos, index=False)
df_itens.to_csv(path_itens, index=False)
df_linhas.to_csv(path_linhas, index=False)

path_clientes, path_pedidos, path_itens, path_linhas
