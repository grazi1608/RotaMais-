const formCadastro = document.querySelector("#form-cadastro");
const campoNome = document.querySelector("#nome");
const campoCpf = document.querySelector("#cpf");
const campoCnh = document.querySelector("#cnh");
const campoTelefone = document.querySelector("#telefone");
const campoEmail = document.querySelector("#email");
const campoDataNascimento = document.querySelector("#data_nascimento");
const campoSenha = document.querySelector("#senha");
const campoConfirmarSenha = document.querySelector("#confirmar_senha");
const mensagem = document.querySelector("#mensagem");

if (obterToken()) {
    window.location.href = "../index.html";
}

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

function mascararCpf(valor) {
    return (valor || "")
        .replace(/\D/g, "")
        .slice(0, 11)
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

function mascararTelefone(valor) {
    const digitos = (valor || "").replace(/\D/g, "").slice(0, 11);
    if (digitos.length <= 10) {
        return digitos
            .replace(/(\d{2})(\d)/, "($1) $2")
            .replace(/(\d{4})(\d{1,4})$/, "$1-$2");
    }
    return digitos
        .replace(/(\d{2})(\d)/, "($1) $2")
        .replace(/(\d{5})(\d{1,4})$/, "$1-$2");
}

campoCpf.addEventListener("input", () => { campoCpf.value = mascararCpf(campoCpf.value); });
campoTelefone.addEventListener("input", () => { campoTelefone.value = mascararTelefone(campoTelefone.value); });

async function cadastrar(evento) {
    evento.preventDefault();

    if (campoSenha.value !== campoConfirmarSenha.value) {
        mostrarMensagem("As senhas não coincidem.", "erro");
        return;
    }

    const dados = {
        nome: campoNome.value,
        cpf: campoCpf.value,
        cnh: campoCnh.value,
        telefone: campoTelefone.value,
        email: campoEmail.value,
        data_nascimento: campoDataNascimento.value || null,
        senha: campoSenha.value,
    };

    try {
        const resposta = await fetch(`${API_BASE}/auth/registrar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });

        const corpo = await resposta.json();

        if (!resposta.ok) {
            mostrarMensagem(corpo.erro || "Não foi possível criar a conta.", "erro");
            return;
        }

        salvarSessao(corpo.token, corpo.motorista);
        window.location.href = "../index.html";
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

formCadastro.addEventListener("submit", cadastrar);
