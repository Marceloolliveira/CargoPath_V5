document.addEventListener("DOMContentLoaded", async function () {
    try {
        const cotacaoId = localStorage.getItem("cotacaoId");
        if (!cotacaoId) {
            alert("ID da cotação não encontrado.");
            return;
        }

        const response = await fetch(`http://127.0.0.1:5000/api/cotacao/resumo/${cotacaoId}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erro ao carregar os dados da cotação.");
        }

        document.querySelector(".IdCotacao").textContent = `Número de Cotação: ${data.cotacao_id}`;
        document.querySelector(".valor").textContent = `Valor: R$ ${data.valor_frete.toFixed(2)}`;
        document.getElementById("dataAgendamento").value = data.data_agendamento || "Não informada";

        preencherDados("remetente", data.remetente);
        preencherDados("destino", data.destino);
        
        document.getElementById("destinoNome").value = data.destino.destinatario_nome || "Não informado";

        document.getElementById("valorCarga").value = data.carga.valor;
        document.getElementById("pesoCarga").value = data.carga.peso;
        document.getElementById("volumesCarga").value = data.carga.volumes;

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

        const embalagemSelecionada = `
            Caixa: ${data.embalagem.caixa || "Não"}<br>
            Palet: ${data.embalagem.palet || "Não"}<br>
            Grade: ${data.embalagem.grade || "Não"}
        `;
        document.getElementById("embalagemSelecionada").innerHTML = `Embalagem Selecionada: <span>${embalagemSelecionada}</span>`;

        configurarBotoes();
    } catch (error) {
        console.error("Erro ao carregar os dados da cotação:", error);
        alert("Erro ao carregar os dados da cotação. Verifique o console.");
    }
});

function preencherDados(tipo, dados) {
    document.getElementById(`${tipo}Rua`).value = dados.rua || "";
    document.getElementById(`${tipo}Numero`).value = dados.numero || "";
    document.getElementById(`${tipo}CEP`).value = dados.cep || "";
    document.getElementById(`${tipo}Cidade`).value = dados.cidade || "";
    document.getElementById(`${tipo}Estado`).value = dados.estado || "";
    document.getElementById(`${tipo}Complemento`).value = dados.complemento || "";
}

function configurarBotoes() {
    document.getElementById("btnPagar").addEventListener("click", function () {
        alert("Funcionalidade de agendamento em desenvolvimento.");
        window.location.href = "/src/app/pages/price/agendar/agendar.html";
    });

    document.getElementById("btnNovaCotacao").addEventListener("click", function () {
        localStorage.removeItem("cotacaoId");
        window.location.href = "/src/app/pages/price/price.html";
    });
}

//sair e limpar localStorage
document.getElementById("sair").addEventListener("click", function() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuarioID");
    localStorage.removeItem("usuarioNome");
    localStorage.removeItem("valorFinalFrete");
    window.location.href = "../../../../../login.html"; // Redireciona para a página de login
});