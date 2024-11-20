document.addEventListener("DOMContentLoaded", async function () {
    try {
        // Recuperar o ID da cotação do localStorage
        const cotacaoId = localStorage.getItem("cotacaoId");
        if (!cotacaoId) {
            alert("ID da cotação não encontrado.");
            return;
        }

        // Fazer requisição para o backend
        const response = await fetch(`http://127.0.0.1:5000/api/cotacao/resumo/${cotacaoId}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erro ao carregar os dados da cotação.");
        }

        // Preencher os dados da cotação
        document.querySelector(".IdCotacao").textContent = `Número de Cotação: ${data.cotacao_id}`;
        document.querySelector(".valor").textContent = `Valor: R$ ${data.valor_frete.toFixed(2)}`;

        // Preencher os dados do remetente
        preencherDados("remetente", data.remetente);

        // Preencher os dados do destino
        preencherDados("destino", data.destino);

        // Preencher os dados da carga
        document.getElementById("valorCarga").value = data.carga.valor;
        document.getElementById("pesoCarga").value = data.carga.peso;
        document.getElementById("volumesCarga").value = data.carga.volumes;

        // Preencher os dados da cubagem
        const cubagem = data.cubagem;
        const cubagemRow = `
            <tr>
                <td>${cubagem.id}</td>
                <td>${cubagem.altura}</td>
                <td>${cubagem.largura}</td>
                <td>${cubagem.comprimento}</td>
                <td>${cubagem.quantidade}</td>
            </tr>
        `;
        document.getElementById("cubagemBody").innerHTML = cubagemRow;

        // Preencher os dados da embalagem
        const embalagemSelecionada = `
            Caixa: ${data.embalagem.caixa || "Não"}<br>
            Palet: ${data.embalagem.palet || "Não"}<br>
            Grade: ${data.embalagem.grade || "Não"}
        `;
        document.getElementById("embalagemSelecionada").innerHTML = `Embalagem Selecionada: <span>${embalagemSelecionada}</span>`;

        // Configurar botões para novas ações
        configurarBotoes();
    } catch (error) {
        console.error("Erro ao carregar os dados da cotação:", error);
        alert("Erro ao carregar os dados da cotação. Verifique o console.");
    }
});

// Função para preencher os dados do remetente/destino
function preencherDados(tipo, dados) {
    document.getElementById(`${tipo}Rua`).value = dados.rua || "";
    document.getElementById(`${tipo}Numero`).value = dados.numero || "";
    document.getElementById(`${tipo}CEP`).value = dados.cep || "";
    document.getElementById(`${tipo}Cidade`).value = dados.cidade || "";
    document.getElementById(`${tipo}Estado`).value = dados.estado || "";
    document.getElementById(`${tipo}Complemento`).value = dados.complemento || "";
}

// Função para configurar botões da página
function configurarBotoes() {
    document.getElementById("btnPagar").addEventListener("click", function () {
        alert("Funcionalidade de agendamento em desenvolvimento.");
    });

    document.getElementById("btnNovaCotacao").addEventListener("click", function () {
        localStorage.removeItem("cotacaoId");
        window.location.href = "/src/app/pages/price/price.html";
    });
}
