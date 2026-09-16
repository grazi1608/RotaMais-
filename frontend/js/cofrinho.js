exigirLogin();

const API_COFRINHO = `${API_BASE}/cofrinho`;

const formObjetivo = document.querySelector("#form-objetivo");
const objetivoId = document.querySelector("#objetivo-id");
const campoNome = document.querySelector("#nome");
const campoValorMeta = document.querySelector("#valor_meta");
const totalGuardadoEl = document.querySelector("#total-guardado");
const listaObjetivos = document.querySelector("#lista-objetivos");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");
const botaoRecarregar = document.querySelector("#botao-recarregar");

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

function formatarMoeda(valor) {
    return `R$ ${parseFloat(valor).toFixed(2).replace(".", ",")}`;
}

function limparFormulario() {
    objetivoId.value = "";
    campoNome.value = "";
    campoValorMeta.value = "";
    tituloFormulario.textContent = "Novo objetivo";
    botaoSalvar.textContent = "Salvar objetivo";
}

async function carregarObjetivos() {
    try {
        const resposta = await fetch(API_COFRINHO, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const dados = await resposta.json();

        totalGuardadoEl.textContent = formatarMoeda(dados.total_guardado);
        listaObjetivos.innerHTML = "";

        if (dados.objetivos.length === 0) {
            listaObjetivos.innerHTML = "<p>Nenhum objetivo cadastrado ainda.</p>";
            return;
        }

        dados.objetivos.forEach((objetivo) => {
            const div = document.createElement("div");
            div.className = "objetivo";
            div.innerHTML = `
                <div class="objetivo-topo">
                    <span class="objetivo-nome">${objetivo.nome}</span>
                    <span>${objetivo.progresso}%</span>
                </div>
                <div class="objetivo-valores">${formatarMoeda(objetivo.valor_guardado)} de ${formatarMoeda(objetivo.valor_meta)}</div>
                <div class="barra-progresso">
                    <div class="barra-progresso-preenchida" style="width: ${objetivo.progresso}%;"></div>
                </div>
                <div class="acoes-tabela" style="margin-top: 10px;">
                    <button onclick="guardarDinheiro(${objetivo.id})">+ Guardar dinheiro</button>
                    <button onclick='prepararEdicao(${JSON.stringify(objetivo)})'>Editar</button>
                    <button class="perigo" onclick="deletarObjetivo(${objetivo.id})">Excluir</button>
                </div>
            `;
            listaObjetivos.appendChild(div);
        });
    } catch (erro) {
        listaObjetivos.innerHTML = "<p>Não foi possível carregar o cofrinho. Verifique se a API está rodando.</p>";
    }
}

function prepararEdicao(objetivo) {
    objetivoId.value = objetivo.id;
    campoNome.value = objetivo.nome;
    campoValorMeta.value = objetivo.valor_meta;
    tituloFormulario.textContent = "Editar objetivo";
    botaoSalvar.textContent = "Atualizar";
    mostrarMensagem("Editando objetivo selecionado.", "sucesso");
}

async function salvarObjetivo(evento) {
    evento.preventDefault();

    const dados = {
        nome: campoNome.value,
        valor_meta: parseFloat(campoValorMeta.value),
    };

    const id = objetivoId.value;
    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_COFRINHO}/${id}` : API_COFRINHO;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: headersAutenticados({ "Content-Type": "application/json" }),
            body: JSON.stringify(dados),
        });

        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao salvar objetivo.", "erro");
            return;
        }

        mostrarMensagem(id ? "Objetivo atualizado." : "Objetivo criado com sucesso.", "sucesso");
        limparFormulario();
        carregarObjetivos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

async function guardarDinheiro(id) {
    const valorTexto = prompt("Quanto você quer guardar neste objetivo? (R$)");
    if (!valorTexto) return;

    const valor = parseFloat(valorTexto.replace(",", "."));
    if (isNaN(valor) || valor <= 0) {
        mostrarMensagem("Valor inválido.", "erro");
        return;
    }

    try {
        const resposta = await fetch(`${API_COFRINHO}/${id}/guardar`, {
            method: "POST",
            headers: headersAutenticados({ "Content-Type": "application/json" }),
            body: JSON.stringify({ valor }),
        });

        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao guardar dinheiro.", "erro");
            return;
        }

        mostrarMensagem("Valor guardado com sucesso!", "sucesso");
        carregarObjetivos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

async function deletarObjetivo(id) {
    if (!confirm("Deseja realmente excluir este objetivo?")) return;

    try {
        const resposta = await fetch(`${API_COFRINHO}/${id}`, {
            method: "DELETE",
            headers: headersAutenticados(),
        });

        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao excluir objetivo.", "erro");
            return;
        }

        mostrarMensagem("Objetivo excluído com sucesso.", "sucesso");
        carregarObjetivos();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

formObjetivo.addEventListener("submit", salvarObjetivo);
botaoCancelar.addEventListener("click", limparFormulario);
botaoRecarregar.addEventListener("click", carregarObjetivos);

carregarObjetivos();
