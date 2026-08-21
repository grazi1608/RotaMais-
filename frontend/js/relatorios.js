const API_RELATORIO_LUCRO = "http://127.0.0.1:5000/relatorios/lucro-por-motorista";

const tabelaRelatorio = document.querySelector("#tabela-relatorio");
const botaoRecarregar = document.querySelector("#botao-recarregar");

async function carregarRelatorio() {
    try {
        const resposta = await fetch(API_RELATORIO_LUCRO);
        const linhas = await resposta.json();

        tabelaRelatorio.innerHTML = "";

        if (linhas.length === 0) {
            tabelaRelatorio.innerHTML = `<tr><td colspan="5">Nenhum motorista cadastrado ainda.</td></tr>`;
            return;
        }

        linhas.forEach((linha) => {
            const tr = document.createElement("tr");
            const corLucro = linha.total_lucro >= 0 ? "green" : "#dc2626";

            tr.innerHTML = `
                <td data-label="Motorista">${linha.motorista_nome}</td>
                <td data-label="Corridas">${linha.total_corridas}</td>
                <td data-label="Faturado">R$ ${linha.total_faturado.toFixed(2)}</td>
                <td data-label="Custo">R$ ${linha.total_custo.toFixed(2)}</td>
                <td data-label="Lucro" style="color: ${corLucro}; font-weight: bold;">R$ ${linha.total_lucro.toFixed(2)}</td>
            `;
            tabelaRelatorio.appendChild(tr);
        });
    } catch (erro) {
        tabelaRelatorio.innerHTML = `<tr><td colspan="5">Não foi possível carregar o relatório. Verifique se a API está rodando.</td></tr>`;
    }
}

botaoRecarregar.addEventListener("click", carregarRelatorio);

carregarRelatorio();
