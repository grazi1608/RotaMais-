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

        const corpo = await resposta.json();

        if (!resposta.ok) {
            mostrarMensagem(corpo.erro || "Não foi possível entrar.", "erro");
            return;
        }

        salvarSessao(corpo.token, corpo.motorista);
        window.location.href = "../index.html";
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

formLogin.addEventListener("submit", entrar);
