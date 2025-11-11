document.addEventListener("DOMContentLoaded", async function () {
    const tableBody = document.querySelector("#historicoTable tbody");
    const userId = localStorage.getItem("usuarioID");

    if (!userId) {
        alert("Usuário não identificado. Faça login novamente.");
        window.location.href = "/login.html";
        return;
    }

    try {
        // Requisição para buscar cotações do histórico (canceladas ou finalizadas)
        const response = await fetch(`http://127.0.0.1:5000/api/cotacao/user/${userId}/historico`);
        const historico = await response.json();

        if (!response.ok) {
            throw new Error(historico.error || historico.message || "Erro ao carregar o histórico.");
        }

        // Preenchendo a tabela com o histórico
        historico.forEach((cotacao) => {
            if (cotacao.status === "cancelado" || cotacao.status === "finalizado") {
                const row = `
                    <tr data-cotacao-id="${cotacao.id}">
                        <td>${cotacao.id || "ID não informado"}</td>
                        <td>${cotacao.remetente || "Remetente não informado"}</td>
                        <td>${cotacao.destino || "Destino não informado"}</td>
                        <td>${cotacao.data_agendamento || "Não informado"}</td>
                        <td>${cotacao.status || "Status não informado"}</td>
                        <td>
                            <button class="detalhes">Detalhes</button>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML("beforeend", row);
            }
        });
    } catch (error) {
        console.error("Erro ao carregar o histórico:", error);
        alert("Erro ao carregar o histórico. Verifique o console.");
    }

    // Event delegation para o botão de "Detalhes"
    tableBody.addEventListener("click", function (event) {
        const button = event.target;

        if (button.classList.contains("detalhes")) {
            const row = button.closest("tr");
            const cotacaoId = row.dataset.cotacaoId; // Recupera o cotacao_id
            verDetalhes(cotacaoId);
        }
    });
});

// Função para visualizar detalhes da cotação (histórico)
function verDetalhes(cotacaoId) {
    localStorage.setItem("cotacaoId", cotacaoId); // Salva cotacao_id no localStorage
    window.location.href = "../collections/detailcollections/detailcollections.html"; // Redireciona para a página de detalhes
}
