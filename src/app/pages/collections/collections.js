document.addEventListener("DOMContentLoaded", async function () {
  const tableBody = document.querySelector("#coletasTable tbody");
  const userId = localStorage.getItem("usuarioID");

  if (!userId) {
      alert("Usuário não identificado. Faça login novamente.");
      window.location.href = "/login.html";
      return;
  }

  try {
      // Requisição para buscar as coletas pelo user_id
      const response = await fetch(`http://127.0.0.1:5000/api/cotacao/user/${userId}/coletas`);
      const coletas = await response.json();

      if (!response.ok) {
          throw new Error(coletas.error || coletas.message || "Erro ao carregar coletas.");
      }

      // Preenchendo a tabela com as coletas
      coletas.forEach((coleta) => {
          const row = `
              <tr data-cotacao-id="${coleta.id}">
                  <td>${coleta.id || "ID não informado"}</td>
                  <td>${coleta.remetente || "Remetente não informado"}</td>
                  <td>${coleta.destino || "Destino não informado"}</td>
                  <td>${coleta.data_agendamento || "Não informado"}</td>
                  <td>${coleta.status || "Status não informado"}</td>
                  <td>
                      <button class="detalhes">Detalhes</button>
                      <button class="cancelar">Cancelar</button>
                  </td>
              </tr>
          `;
          tableBody.insertAdjacentHTML("beforeend", row);
      });

  } catch (error) {
      console.error("Erro ao carregar coletas:", error);
      alert("Erro ao carregar coletas. Verifique o console.");
  }

  // Event delegation para botões de Detalhes e Cancelar
  tableBody.addEventListener("click", async function (event) {
      const button = event.target;

      // Verificar se o clique foi em um botão
      if (button.classList.contains("detalhes")) {
          const row = button.closest("tr");
          const cotacaoId = row.dataset.cotacaoId; // Recupera o cotacao_id
          verDetalhes(cotacaoId);
      }

      if (button.classList.contains("cancelar")) {
          const row = button.closest("tr");
          const cotacaoId = row.dataset.cotacaoId; // Recupera o cotacao_id
          await cancelarColeta(cotacaoId);
      }
  });
});

// Função para visualizar detalhes da cotação (coleta)
function verDetalhes(cotacaoId) {
  localStorage.setItem("cotacaoId", cotacaoId); // Salva cotacao_id no localStorage
  window.location.href = "./detailcollections/detailcollections.html";
}

// Função para cancelar coleta
async function cancelarColeta(cotacaoId) {
  try {
      const response = await fetch(`http://127.0.0.1:5000/api/coletas/${cotacaoId}`, {
          method: "DELETE",
      });

      if (!response.ok) {
          throw new Error("Erro ao cancelar a coleta.");
      }

      alert("Coleta cancelada com sucesso.");
      location.reload();
  } catch (error) {
      console.error("Erro ao cancelar coleta:", error);
      alert("Erro ao cancelar coleta. Verifique o console.");
  }
}
