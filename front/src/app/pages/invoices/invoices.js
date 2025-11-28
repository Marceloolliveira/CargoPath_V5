document.addEventListener("DOMContentLoaded", async function () {
  const tableBody = document.querySelector("#faturasTable tbody");
  const userId = localStorage.getItem("usuarioID");

  if (!userId) {
      alert("Usuário não identificado. Faça login novamente.");
      window.location.href = "/login.html";
      return;
  }

  try {
      const response = await fetch(`http://127.0.0.1:5000/api/user/${userId}/faturas`);
      const faturas = await response.json();

      if (!response.ok) {
          throw new Error(faturas.error || faturas.message || "Erro ao carregar as faturas.");
      }

      faturas.forEach((fatura) => {
          const row = `
              <tr data-cotacao-id="${fatura.id}">
                  <td>${fatura.id || "ID não informado"}</td>
                  <td>${fatura.remetente || "Remetente não informado"}</td>
                  <td>${fatura.destino || "Destino não informado"}</td>
                  <td>${fatura.data_agendamento || "Não informado"}</td>
                  <td>${fatura.status || "Status não informado"}</td>
                  <td>
                      <button class="detalhes">Detalhes</button>
                  </td>
              </tr>
          `;
          tableBody.insertAdjacentHTML("beforeend", row);
      });
  } catch (error) {
      console.error("Erro ao carregar as faturas:", error);
      
  }

  tableBody.addEventListener("click", function (event) {
      const button = event.target;

      if (button.classList.contains("detalhes")) {
          const row = button.closest("tr");
          const cotacaoId = row.dataset.cotacaoId;
          verDetalhes(cotacaoId);
      }
  });
});

function verDetalhes(cotacaoId) {
  localStorage.setItem("cotacaoId", cotacaoId);
  window.location.href = "../collections/detailcollections/detailcollections.html";
}
