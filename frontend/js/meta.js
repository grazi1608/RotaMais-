exigirLogin();

const API_METAS = "http://127.0.0.1:5000/metas";
const API_MOTORISTAS = "http://127.0.0.1:5000/motoristas";

const formMeta = document.querySelector("#form-meta");
const metaId = document.querySelector("#meta-id");
const campoValor = document.querySelector("#valor_meta");
const campoInicio = document.querySelector("#data_inicio");
const campoFim = document.querySelector("#data_fim");
const selectMotorista = document.querySelector("#motorista_id");
const tabelaMetas = document.querySelector("#tabela-metas");
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
    metaId.value = "";
    campoValor.value = "";
    campoInicio.value = "";
    campoFim.value = "";
    selectMotorista.value = "";
    tituloFormulario.textContent = "Estipular Nova Meta";
    botaoSalvar.textContent = "Salvar Meta";
}

async function carregarMotoristas() {
    try {
        const resposta = await fetch(API_MOTORISTAS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const motoristas = await resposta.json();
        selectMotorista.innerHTML = '<option value="">Selecione...</option>';
        motoristas.forEach(m => {
            const opt = document.createElement("option");
            opt.value = m.id;
            opt.textContent = m.nome;
            selectMotorista.appendChild(opt);
        });
    } catch (err) {}
}

async function listarMetas() {
    try {
        const resposta = await fetch(API_METAS, { headers: headersAutenticados() });
        if (await tratarNaoAutenticado(resposta)) return;
        const metas = await resposta.json();
        tabelaMetas.innerHTML = "";

        if (metas.length === 0) {
            tabelaMetas.innerHTML = `<tr><td colspan="5">Nenhuma meta estipulada.</td></tr>`;
            return;
        }

        metas.forEach(m => {
            const linha = document.createElement("tr");
            linha.innerHTML = `
                <td>${m.id}</td>
                <td>R$ ${parseFloat(m.valor_meta).toFixed(2)}</td>
                <td>${m.data_inicio} até ${m.data_fim}</td>
                <td>${m.concluida ? "✅ Concluída" : "⏳ Em andamento"}</td>
                <td>
                    <div class="acoes-tabela">
                        <button class="botao-editar">Editar</button>
                        <button class="perigo botao-excluir">Excluir</button>
                    </div>
                </td>
            `;

            // Anexa os handlers em memória (evita injetar dados não confiáveis em atributos HTML)
            linha.querySelector(".botao-editar").addEventListener("click", () => prepararEdicao(m));
            linha.querySelector(".botao-excluir").addEventListener("click", () => deletarMeta(m.id));

            tabelaMetas.appendChild(linha);
        });
    } catch (err) {
        mostrarMensagem("Erro ao carregar metas.", "erro");
    }
}

function prepararEdicao(m) {
    metaId.value = m.id;
    campoValor.value = m.valor_meta;
    campoInicio.value = m.data_inicio;
    campoFim.value = m.data_fim;
    selectMotorista.value = m.motorista_id || "";
    tituloFormulario.textContent = "Editar Meta";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarMeta(e) {
    e.preventDefault();
    const dados = {
        valor_meta: parseFloat(campoValor.value),
        data_inicio: campoInicio.value,
        data_fim: campoFim.value,
        motorista_id: parseInt(selectMotorista.value)
    };

    const id = metaId.value;
    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_METAS}/${id}` : API_METAS;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: headersAutenticados({ "Content-Type": "application/json" }),
            body: JSON.stringify(dados)
        });
        if (await tratarNaoAutenticado(resposta)) return;

        if (!resposta.ok) return;

        mostrarMensagem("Meta salva com sucesso!", "sucesso");
        limparFormulario();
        listarMetas();
    } catch (err) {}
}

async function deletarMeta(id) {
    if (!confirm("Excluir esta meta?")) return;
    try {
        await fetch(`${API_METAS}/${id}`, { method: "DELETE", headers: headersAutenticados() });
        listarMetas();
    } catch (err) {}
}

formMeta.addEventListener("submit", salvarMeta);
botaoCancelar.addEventListener("click", limparFormulario);
botaoRecarregar.addEventListener("click", () => { carregarMotoristas(); listarMetas(); });

carregarMotoristas();
listarMetas();