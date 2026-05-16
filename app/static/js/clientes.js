console.log("JavaScript carregado com sucesso!");

// =========================
// ELEMENTOS DO HTML
// =========================
// Captura os formulários e listas que serão manipulados pelo JavaScript.

const formCliente = document.getElementById("formCliente");
const listaClientes = document.getElementById("listaClientes");

const formServico = document.getElementById("formServico");
const listaServicos = document.getElementById("listaServicos");
const listaAgenda = document.getElementById("listaAgenda");


// =========================
// CARREGAR CLIENTES
// =========================
// Busca os clientes na API e atualiza a lista na tela.
// Também preenche o select de clientes no cadastro de serviços.

async function carregarClientes() {

    const resposta = await fetch("/clientes");
    const clientes = await resposta.json();

    listaClientes.innerHTML = "";

    const selectCliente = document.getElementById("cliente_id");

    if (selectCliente) {
        selectCliente.innerHTML = `
            <option value="">Selecione o cliente</option>
        `;
    }

    document.getElementById("totalClientes").textContent = clientes.length;

    clientes.forEach(cliente => {

        const item = document.createElement("li");

        item.innerHTML = `
            <span>
                <strong>${cliente.nome}</strong><br>
                ${cliente.email}<br>
                ${cliente.telefone || "Sem telefone"}
            </span>

            <button class="btn-excluir"
                onclick="excluirCliente(${cliente.id})">
                Excluir
            </button>
        `;

        listaClientes.appendChild(item);

        if (selectCliente) {

            const option = document.createElement("option");

            option.value = cliente.id;
            option.textContent = cliente.nome;

            selectCliente.appendChild(option);
        }
    });
}


// =========================
// EXCLUIR CLIENTE
// =========================
// Remove o cliente do banco e recarrega os dados da tela.

async function excluirCliente(id) {

    await fetch(`/clientes/${id}`, {
        method: "DELETE"
    });

    carregarClientes();
    carregarServicos();
}


// =========================
// CADASTRAR CLIENTE
// =========================
// Envia os dados do formulário para a API.

formCliente.addEventListener("submit", async (event) => {

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


// =========================
// CARREGAR SERVIÇOS E AGENDA
// =========================
// Busca os serviços na API, atualiza a lista,
// recalcula o faturamento e monta a agenda.

async function carregarServicos() {

    try {

        const resposta = await fetch("/pedidos");
        const servicos = await resposta.json();

        listaServicos.innerHTML = "";

        if (listaAgenda) {
            listaAgenda.innerHTML = "";
        }

        document.getElementById("totalServicos").textContent = servicos.length;

        const faturamento = servicos.reduce((total, servico) => {
            return total + Number(servico.valor || 0);
        }, 0);

        document.getElementById("faturamentoTotal").textContent =
            `R$ ${faturamento.toFixed(2)}`;

        servicos.forEach(servico => {

            const item = document.createElement("li");

            // Formata a data recebida do backend para o padrão brasileiro.
            const dataFormatada = servico.data_servico
                ? new Date(servico.data_servico).toLocaleString("pt-BR")
                : "Não informada";

            item.innerHTML = `
                <span>
                    <strong>${servico.produto}</strong><br>

                    Cliente: ${servico.cliente}<br>

                    Valor: R$ ${Number(servico.valor).toFixed(2)}<br>

                    Profissional:
                    ${servico.profissional || "Não informado"}<br>

                    Data:
                    ${dataFormatada}
                </span>

                <button class="btn-excluir"
                    onclick="excluirServico(${servico.id})">
                    Excluir
                </button>
            `;

            listaServicos.appendChild(item);

            // A agenda usa os mesmos serviços, mas exibe apenas os que possuem data.
            if (listaAgenda && servico.data_servico) {

                const itemAgenda = document.createElement("li");

                itemAgenda.innerHTML = `
                    <span>
                        <strong>${dataFormatada}</strong><br>

                        ${servico.cliente}<br>

                        ${servico.produto}<br>

                        ${servico.profissional || "Não informado"}
                    </span>
                `;

                listaAgenda.appendChild(itemAgenda);
            }
        });

    } catch (erro) {

        console.error("Erro ao carregar serviços:", erro);
    }
}


// =========================
// CADASTRAR SERVIÇO
// =========================
// Envia o serviço para a API FastAPI.

formServico.addEventListener("submit", async (event) => {

    event.preventDefault();

    const servico = {
        cliente_id: Number(
            document.getElementById("cliente_id").value
        ),

        produto: document.getElementById("produto").value,

        valor: Number(
            document.getElementById("valor").value
        ),

        profissional:
            document.getElementById("profissional").value,

        data_servico:
            document.getElementById("data_servico").value
    };

    try {

        const resposta = await fetch("/pedidos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(servico)
        });

        // Se a API retornar erro, mostra alerta e interrompe o cadastro.
        if (!resposta.ok) {

            const erro = await resposta.text();

            console.error(erro);

            alert("Erro ao cadastrar serviço");

            return;
        }

        formServico.reset();

        carregarServicos();

    } catch (erro) {

        console.error(erro);

        alert("Erro ao conectar com servidor");
    }
});


// =========================
// EXCLUIR SERVIÇO
// =========================
// Remove o serviço e atualiza a lista e agenda.

async function excluirServico(id) {

    await fetch(`/pedidos/${id}`, {
        method: "DELETE"
    });

    carregarServicos();
}


// =========================
// INICIALIZAÇÃO DO SISTEMA
// =========================
// Carrega os dados automaticamente ao abrir o painel.

carregarClientes();
carregarServicos();