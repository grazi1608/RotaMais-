exigirLogin();

const API_CORRIDAS = "http://127.0.0.1:5000/corridas";
const API_MOTORISTAS = "http://127.0.0.1:5000/motoristas";
const API_VEICULOS = "http://127.0.0.1:5000/veiculos";

const formCorrida = document.querySelector("#form-corrida");
const corridaId = document.querySelector("#corrida-id");
const campoValor = document.querySelector("#valor");
const campoDistancia = document.querySelector("#distancia");
const selectMotorista = document.querySelector("#motorista_id");
const selectVeiculo = document.querySelector("#veiculo_id");
const tabelaCorridas = document.querySelector("#tabela-corridas");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");
const botaoRecarregar = document.querySelector("#botao-recarregar");

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

function limparFormulario() {
    corridaId.value = "";
    campoValor.value = "";
    campoDistancia.value = "";
    selectMotorista.value = "";
    selectVeiculo.value = "";
    tituloFormulario.textContent = "Registrar nova corrida";
    botaoSalvar.textContent = "Salvar Corrida";
}

async function carregarMotoristas() {
    try {
        const resposta = await fetch(API_MOTORISTAS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const motoristas = await resposta.json();
        selectMotorista.innerHTML = '<option value="">Selecione um motorista...</option>';
        motoristas.forEach(m => {
            const opt = document.createElement("option");
            opt.value = m.id;
            opt.textContent = m.nome;
            selectMotorista.appendChild(opt);
        });
    } catch (err) {
        mostrarMensagem("Erro ao carregar motoristas.", "erro");
    }
}

async function carregarVeiculos() {
    try {
        const resposta = await fetch(API_VEICULOS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const veiculos = await resposta.json();
        selectVeiculo.innerHTML = '<option value="">Selecione um veículo...</option>';
        veiculos.forEach(v => {
            const opt = document.createElement("option");
            opt.value = v.id;
            opt.textContent = `${v.modelo} - ${v.placa}`;
            selectVeiculo.appendChild(opt);
        });
    } catch (err) {
        mostrarMensagem("Erro ao carregar veículos.", "erro");
    }
}

async function listarCorridas() {
    try {
        const resposta = await fetch(API_CORRIDAS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const corridas = await resposta.json();
        tabelaCorridas.innerHTML = "";

        if (corridas.length === 0) {
            tabelaCorridas.innerHTML = `<tr><td colspan="7">Nenhuma corrida registrada.</td></tr>`;
            return;
        }

        corridas.forEach(c => {
            const linha = document.createElement("tr");
            linha.innerHTML = `
                <td data-label="ID">${c.id}</td>
                <td data-label="Data/Hora">${c.data_hora}</td>
                <td data-label="Valor">R$ ${parseFloat(c.valor).toFixed(2)}</td>
                <td data-label="Custo">R$ ${parseFloat(c.custo_estimado).toFixed(2)}</td>
                <td data-label="Lucro" style="color: green; font-weight: bold;">R$ ${parseFloat(c.lucro).toFixed(2)}</td>
                <td data-label="Distância">${c.distancia} km</td>
                <td data-label="Ações">
                    <div class="acoes-tabela">
                        <button onclick='prepararEdicao(${JSON.stringify(c)})'>Editar</button>
                        <button class="perigo" onclick="deletarCorrida(${c.id})">Excluir</button>
                    </div>
                </td>
            `;
            tabelaCorridas.appendChild(linha);
        });
    } catch (err) {
        mostrarMensagem("Erro ao carregar o histórico de corridas.", "erro");
    }
}

function prepararEdicao(corrida) {
    corridaId.value = corrida.id;
    campoValor.value = corrida.valor;
    campoDistancia.value = corrida.distancia;
    selectMotorista.value = corrida.motorista_id || "";
    selectVeiculo.value = corrida.veiculo_id || "";
    tituloFormulario.textContent = "Editar corrida";
    botaoSalvar.textContent = "Atualizar";
    mostrarMensagem("Editando corrida selecionada.", "sucesso");
}

async function salvarCorrida(e) {
    e.preventDefault();
    const dados = {
        valor: parseFloat(campoValor.value),
        distancia: parseFloat(campoDistancia.value),
        motorista_id: parseInt(selectMotorista.value),
        veiculo_id: parseInt(selectVeiculo.value)
    };

    const id = corridaId.value;
    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_CORRIDAS}/${id}` : API_CORRIDAS;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: headersAutenticados({ "Content-Type": "application/json" }),
            body: JSON.stringify(dados)
        });
        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao salvar corrida.", "erro");
            return;
        }

        mostrarMensagem(id ? "Corrida atualizada com sucesso." : "Corrida registrada com sucesso!", "sucesso");
        limparFormulario();
        listarCorridas();
    } catch (err) {
        mostrarMensagem("Erro de conexão com o servidor.", "erro");
    }
}

async function deletarCorrida(id) {
    if (!confirm("Remover esta corrida do histórico?")) return;
    try {
        const resposta = await fetch(`${API_CORRIDAS}/${id}`, { method: "DELETE", headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        if (resposta.ok) {
            mostrarMensagem("Corrida excluída com sucesso.", "sucesso");
            listarCorridas();
        }
    } catch (err) {
        mostrarMensagem("Erro ao excluir a corrida.", "erro");
    }
}

formCorrida.addEventListener("submit", salvarCorrida);
botaoCancelar.addEventListener("click", limparFormulario);
botaoRecarregar.addEventListener("click", () => {
    carregarMotoristas();
    carregarVeiculos();
    listarCorridas();
});

// Inicializar dados na página
carregarMotoristas();
carregarVeiculos();
listarCorridas();
