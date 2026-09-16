// Funções compartilhadas de autenticação — usadas por todas as páginas.
const API_BASE = "http://127.0.0.1:5000";
const CHAVE_TOKEN = "rotamais_token";
const CHAVE_MOTORISTA = "rotamais_motorista";

function estaDentroDePagina() {
    return window.location.pathname.includes("/paginas/");
}

function caminhoLogin() {
    return estaDentroDePagina() ? "login.html" : "paginas/login.html";
}

function caminhoInicio() {
    return estaDentroDePagina() ? "../index.html" : "index.html";
}

function obterToken() {
    return localStorage.getItem(CHAVE_TOKEN);
}

function obterMotoristaLogado() {
    const dados = localStorage.getItem(CHAVE_MOTORISTA);
    return dados ? JSON.parse(dados) : null;
}

function salvarSessao(token, motorista) {
    localStorage.setItem(CHAVE_TOKEN, token);
    localStorage.setItem(CHAVE_MOTORISTA, JSON.stringify(motorista));
}

function limparSessao() {
    localStorage.removeItem(CHAVE_TOKEN);
    localStorage.removeItem(CHAVE_MOTORISTA);
}

// Chame no topo de toda página protegida: redireciona para o login se não houver sessão.
function exigirLogin() {
    if (!obterToken()) {
        window.location.href = caminhoLogin();
    }
}

// Monta os headers padrão (com o token) pra usar no fetch.
function headersAutenticados(extra = {}) {
    return {
        ...extra,
        "Authorization": `Bearer ${obterToken()}`,
    };
}

// Verifica se a resposta indica sessão expirada/inválida; se sim, desloga e retorna true.
async function tratarNaoAutenticado(resposta) {
    if (resposta.status === 401) {
        limparSessao();
        window.location.href = caminhoLogin();
        return true;
    }
    return false;
}

async function sair() {
    try {
        await fetch(`${API_BASE}/auth/logout`, {
            method: "POST",
            headers: headersAutenticados(),
        });
    } catch (erro) {
        // Mesmo se der erro de conexão, limpamos a sessão local.
    }
    limparSessao();
    window.location.href = caminhoLogin();
}

function configurarBotaoSair() {
    const botao = document.querySelector("#botao-sair");
    if (botao) {
        botao.addEventListener("click", sair);
    }
}

document.addEventListener("DOMContentLoaded", configurarBotaoSair);
