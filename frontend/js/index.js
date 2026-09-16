exigirLogin();

const motorista = obterMotoristaLogado();
const tituloBoasVindas = document.querySelector("#titulo-boas-vindas");

if (motorista && tituloBoasVindas) {
    tituloBoasVindas.textContent = `Olá, ${motorista.nome.split(" ")[0]}!`;
}
