console.log("JavaScript carregado com sucesso!");

const formCliente = document.getElementById("formCliente");
const listaClientes = document.getElementById("listaClientes");

const formServico = document.getElementById("formServico");
const listaServicos = document.getElementById("listaServicos");
const listaAgenda = document.getElementById("listaAgenda");

async function carregarClientes() {
    const resposta = await fetch("/clientes");
    const clientes = await resposta.json();

    listaClientes.innerHTML = "";

    const selectCliente = document.getElementById("cliente_id");
    selectCliente.innerHTML = '<option value="">Selecione o cliente</option>';

    document.getElementById("totalClientes").textContent = clientes.length;

    clientes.forEach(cliente => {
        const item = document.createElement("li");

        item.innerHTML = `
            <span>
                <strong>ID:</strong> ${cliente.id}<br>
                <strong>Nome:</strong> ${cliente.nome}<br>
                <strong>Email:</strong> ${cliente.email}<br>
                <strong>Telefone:</strong> ${cliente.telefone || "Não informado"}
            </span>

            <button class="btn-excluir" onclick="excluirCliente(${cliente.id})">Excluir</button>
        `;

        listaClientes.appendChild(item);

        const option = document.createElement("option");
        option.value = cliente.id;
        option.textContent = `${cliente.nome} - ${cliente.telefone || "Sem telefone"}`;
        selectCliente.appendChild(option);
    });
}

async function excluirCliente(id) {
    await fetch(`/clientes/${id}`, {
        method: "DELETE"
    });

    carregarClientes();
    carregarServicos();
}

formCliente.addEventListener("submit", async function(event) {
    event.preventDefault();

    const cliente = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        telefone: document.getElementById("telefone").value
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

async function carregarServicos() {
    const resposta = await fetch("/pedidos");
    const servicos = await resposta.json();

    listaServicos.innerHTML = "";

    if (listaAgenda) {
        listaAgenda.innerHTML = "";
    }

    document.getElementById("totalServicos").textContent = servicos.length;

    const faturamento = servicos.reduce((total, servico) => {
        return total + Number(servico.valor);
    }, 0);

    document.getElementById("faturamentoTotal").textContent = `R$ ${faturamento.toFixed(2)}`;

    servicos.forEach(servico => {
        const item = document.createElement("li");

        const dataFormatada = servico.data_servico
            ? new Date(servico.data_servico).toLocaleDateString("pt-BR")
            : "Não informada";

        item.innerHTML = `
            <span>
                <strong>ID:</strong> ${servico.id}<br>
                <strong>Cliente:</strong> ${servico.cliente}<br>
                <strong>Serviço:</strong> ${servico.produto}<br>
                <strong>Valor:</strong> R$ ${Number(servico.valor).toFixed(2)}<br>
                <strong>Profissional:</strong> ${servico.profissional || "Não informado"}<br>
                <strong>Data do serviço:</strong> ${dataFormatada}
            </span>

            <button class="btn-excluir" onclick="excluirServico(${servico.id})">Excluir</button>
        `;

        listaServicos.appendChild(item);

        if (listaAgenda && servico.data_servico) {
            const itemAgenda = document.createElement("li");

            itemAgenda.innerHTML = `
                <span>
                    <strong>Data:</strong> ${dataFormatada}<br>
                    <strong>Cliente:</strong> ${servico.cliente}<br>
                    <strong>Serviço:</strong> ${servico.produto}<br>
                    <strong>Profissional:</strong> ${servico.profissional || "Não informado"}<br>
                    <strong>Valor:</strong> R$ ${Number(servico.valor).toFixed(2)}
                </span>
            `;

            listaAgenda.appendChild(itemAgenda);
        }
    });
}

formServico.addEventListener("submit", async function(event) {
    event.preventDefault();

    const servico = {
        cliente_id: Number(document.getElementById("cliente_id").value),
        produto: document.getElementById("produto").value,
        valor: Number(document.getElementById("valor").value),
        profissional: document.getElementById("profissional").value,
        data_servico: document.getElementById("data_servico").value
    };

    await fetch("/pedidos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(servico)
    });

    formServico.reset();
    carregarServicos();
});

async function excluirServico(id) {
    await fetch(`/pedidos/${id}`, {
        method: "DELETE"
    });

    carregarServicos();
}

carregarClientes();
carregarServicos();