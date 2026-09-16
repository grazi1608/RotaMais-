exigirLogin();

const API_GASTOS = `${API_BASE}/gastos`;
const API_VEICULOS = `${API_BASE}/veiculos`;

const formGasto = document.querySelector("#form-gasto");
const gastoId = document.querySelector("#gasto-id");
const campoTipo = document.querySelector("#tipo");
const campoValor = document.querySelector("#valor");
const campoDescricao = document.querySelector("#descricao");
const selectVeiculo = document.querySelector("#veiculo_id");
const tabelaGastos = document.querySelector("#tabela-gastos");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");
const botaoRecarregar = document.querySelector("#botao-recarregar");

const rotulosTipo = {
    combustivel: "Combustível",
    manutencao: "Manutenção",
    outro: "Outro",
};

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

function limparFormulario() {
    gastoId.value = "";
    campoTipo.value = "combustivel";
    campoValor.value = "";
    campoDescricao.value = "";
    selectVeiculo.value = "";
    tituloFormulario.textContent = "Registrar novo gasto";
    botaoSalvar.textContent = "Salvar Gasto";
}

async function carregarVeiculos() {
    try {
        const resposta = await fetch(API_VEICULOS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const veiculos = await resposta.json();

        selectVeiculo.innerHTML = '<option value="">Nenhum veículo específico</option>';
        veiculos.forEach(v => {
            const opt = document.createElement("option");
            opt.value = v.id;
            opt.textContent = `${v.modelo} - ${v.placa}`;
            selectVeiculo.appendChild(opt);
        });
    } catch (erro) {
        mostrarMensagem("Erro ao carregar veículos.", "erro");
    }
}

async function listarGastos() {
    try {
        const resposta = await fetch(API_GASTOS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const gastos = await resposta.json();

        tabelaGastos.innerHTML = "";

        if (gastos.length === 0) {
            tabelaGastos.innerHTML = `<tr><td colspan="5">Nenhum gasto registrado ainda.</td></tr>`;
            return;
        }

        gastos.forEach((gasto) => {
            const linha = document.createElement("tr");
            const dataFormatada = gasto.data ? new Date(gasto.data).toLocaleDateString("pt-BR") : "-";

            linha.innerHTML = `
                <td data-label="Data">${dataFormatada}</td>
                <td data-label="Tipo">${rotulosTipo[gasto.tipo] || gasto.tipo}</td>
                <td data-label="Descrição">${gasto.descricao || "-"}</td>
                <td data-label="Valor">R$ ${parseFloat(gasto.valor).toFixed(2)}</td>
                <td data-label="Ações">
                    <div class="acoes-tabela">
                        <button onclick='prepararEdicao(${JSON.stringify(gasto)})'>Editar</button>
                        <button class="perigo" onclick="deletarGasto(${gasto.id})">Excluir</button>
                    </div>
                </td>
            `;
            tabelaGastos.appendChild(linha);
        });
    } catch (erro) {
        mostrarMensagem("Não foi possível carregar os gastos. Verifique se a API está rodando.", "erro");
    }
}

function prepararEdicao(gasto) {
    gastoId.value = gasto.id;
    campoTipo.value = gasto.tipo;
    campoValor.value = gasto.valor;
    campoDescricao.value = gasto.descricao || "";
    selectVeiculo.value = gasto.veiculo_id || "";
    tituloFormulario.textContent = "Editar gasto";
    botaoSalvar.textContent = "Atualizar";
    mostrarMensagem("Editando gasto selecionado.", "sucesso");
}

async function salvarGasto(evento) {
    evento.preventDefault();

    const dados = {
        tipo: campoTipo.value,
        valor: parseFloat(campoValor.value),
        descricao: campoDescricao.value || null,
        veiculo_id: selectVeiculo.value ? parseInt(selectVeiculo.value) : null,
    };

    const id = gastoId.value;
    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_GASTOS}/${id}` : API_GASTOS;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: headersAutenticados({ "Content-Type": "application/json" }),
            body: JSON.stringify(dados),
        });

        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao salvar gasto.", "erro");
            return;
        }

        mostrarMensagem(id ? "Gasto atualizado com sucesso." : "Gasto registrado com sucesso.", "sucesso");
        limparFormulario();
        listarGastos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

async function deletarGasto(id) {
    if (!confirm("Deseja realmente excluir este gasto?")) return;

    try {
        const resposta = await fetch(`${API_GASTOS}/${id}`, {
            method: "DELETE",
            headers: headersAutenticados(),
        });

        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao excluir gasto.", "erro");
            return;
        }

        mostrarMensagem("Gasto excluído com sucesso.", "sucesso");
        listarGastos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

formGasto.addEventListener("submit", salvarGasto);
botaoCancelar.addEventListener("click", limparFormulario);
botaoRecarregar.addEventListener("click", () => {
    carregarVeiculos();
    listarGastos();
});

carregarVeiculos();
listarGastos();
