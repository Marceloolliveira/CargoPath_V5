document.addEventListener("DOMContentLoaded", async function () {
  const tableBody = document.querySelector("#coletasTable tbody");
  const userId = localStorage.getItem("usuarioID");

  if (!userId) {
      alert("Usuário não identificado. Faça login novamente.");
      window.location.href = "/login.html";
      return;
  }

  try {
      const response = await fetch(`http://127.0.0.1:5000/api/cotacao/user/${userId}/coletas`);
      const coletas = await response.json();

      if (!response.ok) {
          throw new Error(coletas.error || coletas.message || "Erro ao carregar coletas.");
      }

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

  tableBody.addEventListener("click", async function (event) {
      const button = event.target;

      if (button.classList.contains("detalhes")) {
          const row = button.closest("tr");
          const cotacaoId = row.dataset.cotacaoId;
          verDetalhes(cotacaoId);
      }

      if (button.classList.contains("cancelar")) {
          const row = button.closest("tr");
          const cotacaoId = row.dataset.cotacaoId;
          await cancelarColeta(row, cotacaoId);
      }
  });
});

function verDetalhes(cotacaoId) {
  localStorage.setItem("cotacaoId", cotacaoId);
  window.location.href = "./detailcollections/detailcollections.html";
}

async function cancelarColeta(row, cotacaoId) {
  const confirmacao = confirm("Tem certeza de que deseja cancelar esta cotação?");
  if (!confirmacao) return;

  const userId = localStorage.getItem("usuarioID");

  try {
      const response = await fetch(`http://127.0.0.1:5000/api/cotacao/${cotacaoId}`, {
          method: "PUT",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              descricao: "Cotação cancelada",
              status: "cancelado",
              user_id: userId,
          }),
      });

      if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Erro ao cancelar a coleta.");
      }

      const data = await response.json();
      alert(data.message || "Cotação cancelada com sucesso.");

      row.remove();
  } catch (error) {
      console.error("Erro ao cancelar a coleta:", error);
      alert("Erro ao cancelar a coleta. Verifique o console.");
  }
}

