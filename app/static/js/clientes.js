console.log("JavaScript carregado com sucesso!");

const formCliente = document.getElementById("formCliente");
const listaClientes = document.getElementById("listaClientes");

async function carregarClientes() {
    const resposta = await fetch("/clientes");
    const clientes = await resposta.json();

    listaClientes.innerHTML = "";

    document.getElementById("totalClientes").textContent = clientes.length;

    clientes.forEach(cliente => {
        const item = document.createElement("li");

        item.innerHTML = `
            <span>${cliente.id} - ${cliente.nome} - ${cliente.email} - ${cliente.idade} anos</span>
            <button class="btn-excluir" onclick="excluirCliente(${cliente.id})">Excluir</button>
        `;

        listaClientes.appendChild(item);
    });
}

async function excluirCliente(id) {
    await fetch(`/clientes/${id}`, {
        method: "DELETE"
    });

    carregarClientes();
}

formCliente.addEventListener("submit", async function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const idade = document.getElementById("idade").value;

    const cliente = {
        nome: nome,
        email: email,
        idade: Number(idade)
    };

    await fetch("/clientes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(cliente)
    });

    formCliente.reset();
    carregarClientes();
});

carregarClientes();

const formPedido = document.getElementById("formPedido");
const listaPedidos = document.getElementById("listaPedidos");

async function carregarPedidos() {
    const resposta = await fetch("/pedidos");
    const pedidos = await resposta.json();

    listaPedidos.innerHTML = "";

    document.getElementById("totalServicos").textContent = pedidos.length;

const faturamento = pedidos.reduce((total, pedido) => total + Number(pedido.valor), 0);

document.getElementById("faturamentoTotal").textContent = `R$ ${faturamento.toFixed(2)}`;

    pedidos.forEach(pedido => {
        const item = document.createElement("li");

        item.innerHTML = `
    <span>${pedido.id} - ${pedido.cliente} - ${pedido.produto} - R$ ${pedido.valor}</span>
    <button class="btn-excluir" onclick="excluirPedido(${pedido.id})">Excluir</button>
`;

        listaPedidos.appendChild(item);
    });
}

formPedido.addEventListener("submit", async function(event) {
    event.preventDefault();

    const cliente_id = document.getElementById("cliente_id").value;
    const produto = document.getElementById("produto").value;
    const valor = document.getElementById("valor").value;

    const pedido = {
        cliente_id: Number(cliente_id),
        produto: produto,
        valor: Number(valor)
    };

    await fetch("/pedidos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pedido)
    });

    formPedido.reset();
    carregarPedidos();
});

carregarPedidos();

async function excluirPedido(id) {
    await fetch(`/pedidos/${id}`, {
        method: "DELETE"
    });

    carregarPedidos();
}

