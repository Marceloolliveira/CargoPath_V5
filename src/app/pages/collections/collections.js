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
              <tr>
                  <td>${coleta.id}</td>
                  <td>${coleta.remetente}</td>
                  <td>${coleta.destino}</td>
                  <td>${coleta.data_agendamento || "Não informado"}</td>
                  <td>${coleta.status}</td>
                  <td>
                      <button class="detalhes" onclick="verDetalhes(${coleta.id})">Detalhes</button>
                      <button class="cancelar" onclick="cancelarColeta(${coleta.id})">Cancelar</button>
                  </td>
              </tr>
          `;
          tableBody.insertAdjacentHTML("beforeend", row);
      });
  } catch (error) {
      console.error("Erro ao carregar coletas:", error);
      alert("Erro ao carregar coletas. Verifique o console.");
  }
});

// Função para visualizar detalhes da coleta
function verDetalhes(id) {
  localStorage.setItem("coletaId", id);
  window.location.href = "/src/app/pages/collections/detalhes/detalhes.html";
}

// Função para cancelar coleta
async function cancelarColeta(id) {
  try {
      const response = await fetch(`http://127.0.0.1:5000/api/coletas/${id}`, {
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
