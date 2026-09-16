exigirLogin();

const API_VEICULOS = "http://127.0.0.1:5000/veiculos";
const API_MOTORISTAS = "http://127.0.0.1:5000/motoristas";

const formVeiculo = document.querySelector("#form-veiculo");
const veiculoId = document.querySelector("#veiculo-id");
const campoModelo = document.querySelector("#modelo");
const campoPlaca = document.querySelector("#placa");
const campoConsumo = document.querySelector("#consumo_por_km");
const selectMotorista = document.querySelector("#motorista_id");
const tabelaVeiculos = document.querySelector("#tabela-veiculos");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");
const botaoRecarregar = document.querySelector("#botao-recarregar");

let motoristasCache = [];

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

function nomeMotorista(motoristaId) {
    const motorista = motoristasCache.find((m) => m.id === motoristaId);
    return motorista ? motorista.nome : `#${motoristaId}`;
}

function limparFormulario() {
    veiculoId.value = "";
    campoModelo.value = "";
    campoPlaca.value = "";
    campoConsumo.value = "";
    selectMotorista.value = "";
    tituloFormulario.textContent = "Cadastrar veículo";
    botaoSalvar.textContent = "Salvar";
}

async function carregarMotoristas() {
    try {
        const resposta = await fetch(API_MOTORISTAS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const motoristas = await resposta.json();
        motoristasCache = motoristas;

        selectMotorista.innerHTML = '<option value="">Selecione um motorista...</option>';

        motoristas.forEach(motorista => {
            const opcao = document.createElement("option");
            opcao.value = motorista.id;
            opcao.textContent = `${motorista.nome} (ID: ${motorista.id})`;
            selectMotorista.appendChild(opcao);
        });
    } catch (erro) {
        mostrarMensagem("Erro ao carregar a lista de motoristas.", "erro");
    }
}

async function listarVeiculos() {
    try {
        const resposta = await fetch(API_VEICULOS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const veiculos = await resposta.json();

        tabelaVeiculos.innerHTML = "";

        if (veiculos.length === 0) {
            tabelaVeiculos.innerHTML = `
                <tr>
                    <td colspan="6">Nenhum veículo cadastrado.</td>
                </tr>
            `;
            return;
        }

        veiculos.forEach((veiculo) => {
            const linha = document.createElement("tr");

            linha.innerHTML = `
                <td data-label="ID">${veiculo.id}</td>
                <td data-label="Modelo">${veiculo.modelo}</td>
                <td data-label="Placa">${veiculo.placa}</td>
                <td data-label="Consumo">R$ ${parseFloat(veiculo.consumo_por_km).toFixed(2)}</td>
                <td data-label="Motorista">${nomeMotorista(veiculo.motorista_id)}</td>
                <td data-label="Ações">
                    <div class="acoes-tabela">
                        <button onclick='prepararEdicao(${JSON.stringify(veiculo)})'>Editar</button>
                        <button class="perigo" onclick="deletarVeiculo(${veiculo.id})">Excluir</button>
                    </div>
                </td>
            `;

            tabelaVeiculos.appendChild(linha);
        });
    } catch (erro) {
        mostrarMensagem("Não foi possível carregar os veículos. Verifique se a API está ativa.", "erro");
    }
}

function prepararEdicao(veiculo) {
    veiculoId.value = veiculo.id;
    campoModelo.value = veiculo.modelo;
    campoPlaca.value = veiculo.placa;
    campoConsumo.value = veiculo.consumo_por_km;
    selectMotorista.value = veiculo.motorista_id || "";
    tituloFormulario.textContent = "Editar veículo";
    botaoSalvar.textContent = "Atualizar";
    mostrarMensagem("Editando veículo selecionado.", "sucesso");
}

async function salvarVeiculo(evento) {
    evento.preventDefault();

    const dados = {
        modelo: campoModelo.value,
        placa: campoPlaca.value,
        consumo_por_km: parseFloat(campoConsumo.value),
        motorista_id: parseInt(selectMotorista.value)
    };

    const id = veiculoId.value;
    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_VEICULOS}/${id}` : API_VEICULOS;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: headersAutenticados({ "Content-Type": "application/json" }),
            body: JSON.stringify(dados),
        });
        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao salvar veículo.", "erro");
            return;
        }

        mostrarMensagem(id ? "Veículo atualizado com sucesso." : "Veículo cadastrado com sucesso.", "sucesso");
        limparFormulario();
        listarVeiculos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

async function deletarVeiculo(id) {
    const confirmar = confirm("Deseja realmente excluir este veículo?");

    if (!confirmar) {
        return;
    }

    try {
        const resposta = await fetch(`${API_VEICULOS}/${id}`, {
            method: "DELETE",
            headers: headersAutenticados(),
        });
        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao excluir veículo.", "erro");
            return;
        }

        mostrarMensagem("Veículo excluído com sucesso.", "sucesso");
        listarVeiculos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

formVeiculo.addEventListener("submit", salvarVeiculo);
botaoCancelar.addEventListener("click", limparFormulario);
botaoRecarregar.addEventListener("click", () => {
    carregarMotoristas();
    listarVeiculos();
});

// Inicialização da página
carregarMotoristas().then(listarVeiculos);
