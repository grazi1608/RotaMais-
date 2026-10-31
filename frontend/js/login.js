const formLogin = document.querySelector("#form-login");
const campoIdentificador = document.querySelector("#identificador");
const campoSenha = document.querySelector("#senha");
const mensagem = document.querySelector("#mensagem");

// Se já estiver logado, vai direto para a página inicial.
if (obterToken()) {
    window.location.href = "../index.html";
}

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

async function entrar(evento) {
    evento.preventDefault();

    const dados = {
        identificador: campoIdentificador.value,
        senha: campoSenha.value,
    };

    try {
        const resposta = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });

        const corpo = await lerJsonSeguro(resposta);

        if (!resposta.ok) {
            const padrao = resposta.status >= 500
                ? "Erro interno no servidor. Veja o terminal do backend (provável banco de dados desatualizado)."
                : "Não foi possível entrar.";
            mostrarMensagem(corpo.erro || padrao, "erro");
            return;
        }

        salvarSessao(corpo.token, corpo.motorista);
        window.location.href = "../index.html";
    } catch (erro) {
        mostrarMensagem(`Não foi possível falar com a API em ${API_BASE}. Confira se o backend está rodando (python backend/app.py) e abra o site em http://127.0.0.1:5000.`, "erro");
    }
}

formLogin.addEventListener("submit", entrar);
