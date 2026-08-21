const API_URL = "http://127.0.0.1:5000/motoristas";

const formMotorista = document.querySelector("#form-motorista");
const motoristaId = document.querySelector("#motorista-id");
const campoNome = document.querySelector("#nome");
const campoCpf = document.querySelector("#cpf");
const campoCnh = document.querySelector("#cnh");
const campoTelefone = document.querySelector("#telefone");
const campoEmail = document.querySelector("#email");
const tabelaMotoristas = document.querySelector("#tabela-motoristas");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");
const botaoRecarregar = document.querySelector("#botao-recarregar");

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
}

// Formata dígitos no padrão de CPF: 123.456.789-00
function mascararCpf(valor) {
    return (valor || "")
        .replace(/\D/g, "")            // remove tudo que não for número
        .slice(0, 11)                  // limita a 11 dígitos
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

// Formata dígitos no padrão de telefone: (11) 9999-9999 ou (11) 99999-9999
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

// Aplica a máscara enquanto o usuário digita
campoCpf.addEventListener("input", () => {
    campoCpf.value = mascararCpf(campoCpf.value);
});

campoTelefone.addEventListener("input", () => {
    campoTelefone.value = mascararTelefone(campoTelefone.value);
});

function limparFormulario() {
    motoristaId.value = "";
    campoNome.value = "";
    campoCpf.value = "";
    campoCnh.value = "";
    campoTelefone.value = "";
    campoEmail.value = "";
    tituloFormulario.textContent = "Cadastrar motorista";
    botaoSalvar.textContent = "Salvar";
}

async function listarMotoristas() {
    try {
        const resposta = await fetch(API_URL);
        const motoristas = await resposta.json();

        tabelaMotoristas.innerHTML = "";

        if (motoristas.length === 0) {
            tabelaMotoristas.innerHTML = `
                <tr>
                    <td colspan="5">Nenhum motorista cadastrado.</td>
                </tr>
            `;
            return;
        }

        motoristas.forEach((motorista) => {
            const linha = document.createElement("tr");

            linha.innerHTML = `
                <td data-label="ID">${motorista.id}</td>
                <td data-label="Nome">${motorista.nome}</td>
                <td data-label="CPF">${mascararCpf(motorista.cpf)}</td>
                <td data-label="CNH">${motorista.cnh}</td>
                <td data-label="Ações">
                    <div class="acoes-tabela">
                        <button onclick='prepararEdicao(${JSON.stringify(motorista)})'>Editar</button>
                        <button class="perigo" onclick="deletarMotorista(${motorista.id})">Excluir</button>
                    </div>
                </td>
            `;

            tabelaMotoristas.appendChild(linha);
        });
    } catch (erro) {
        mostrarMensagem("Não foi possível carregar os motoristas. Verifique se a API está rodando.", "erro");
    }
}

function prepararEdicao(motorista) {
    motoristaId.value = motorista.id;
    campoNome.value = motorista.nome;
    campoCpf.value = mascararCpf(motorista.cpf);
    campoCnh.value = motorista.cnh;
    campoTelefone.value = mascararTelefone(motorista.telefone || "");
    campoEmail.value = motorista.email || "";
    tituloFormulario.textContent = "Editar motorista";
    botaoSalvar.textContent = "Atualizar";
    mostrarMensagem("Editando motorista selecionado.", "sucesso");
}

async function salvarMotorista(evento) {
    evento.preventDefault();

    const dados = {
        nome: campoNome.value,
        cpf: campoCpf.value,
        cnh: campoCnh.value,
        telefone: campoTelefone.value,
        email: campoEmail.value
    };

    const id = motoristaId.value;
    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/${id}` : API_URL;

    try {
        const resposta = await fetch(url, {
            method: metodo,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(dados),
        });

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao salvar motorista.", "erro");
            return;
        }

        mostrarMensagem(id ? "Motorista atualizado com sucesso." : "Motorista cadastrado com sucesso.", "sucesso");
        limparFormulario();
        listarMotoristas();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

async function deletarMotorista(id) {
    const confirmar = confirm("Deseja realmente excluir este motorista?");

    if (!confirmar) {
        return;
    }

    try {
        const resposta = await fetch(`${API_URL}/${id}`, {
            method: "DELETE",
        });

        if (!resposta.ok) {
            const erro = await resposta.json();
            mostrarMensagem(erro.erro || "Erro ao excluir motorista.", "erro");
            return;
        }

        mostrarMensagem("Motorista excluído com sucesso.", "sucesso");
        listarMotoristas();
    } catch (erro) {
        mostrarMensagem("Erro de conexão com a API.", "erro");
    }
}

formMotorista.addEventListener("submit", salvarMotorista);
botaoCancelar.addEventListener("click", limparFormulario);
botaoRecarregar.addEventListener("click", listarMotoristas);

listarMotoristas();
