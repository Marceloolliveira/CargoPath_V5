document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const listaColetasAdm = document.getElementById("listaColetasAdm");

  // Função para carregar todas as coletas ou coletas filtradas
  async function carregarColetas(filtro = "") {
      try {
          const response = await fetch(`http://127.0.0.1:5000/api/admin/coletas?query=${filtro}`);
          const coletas = await response.json();

          if (response.ok) {
              listaColetasAdm.innerHTML = ""; // Limpa a lista antes de preencher

              coletas.forEach(coleta => {
                  const divColeta = document.createElement("div");
                  divColeta.classList.add("coleta-item");
                  divColeta.innerHTML = `
                      <h3>ID da Coleta: ${coleta.coleta_id}</h3>
                      <p><strong>Nome:</strong> ${coleta.nome}</p>
                      <p><strong>Email:</strong> ${coleta.email}</p>
                      <p><strong>CPF:</strong> ${coleta.cpf}</p>
                      <p><strong>Status:</strong> 
                          <select class="status-select" data-id="${coleta.coleta_id}">
                              <option value="andamento" ${coleta.status === "andamento" ? "selected" : ""}>Em Andamento</option>
                              <option value="concluido" ${coleta.status === "concluido" ? "selected" : ""}>Concluído</option>
                              <option value="cancelado" ${coleta.status === "cancelado" ? "selected" : ""}>Cancelado</option>
                          </select>
                      </p>
                      <button class="btn btn-danger btn-cancelar" data-id="${coleta.coleta_id}">Cancelar Agendamento</button>
                  `;
                  listaColetasAdm.appendChild(divColeta);
              });

              // Adiciona eventos para mudar status
              document.querySelectorAll(".status-select").forEach(select => {
                  select.addEventListener("change", atualizarStatus);
              });

              // Adiciona eventos para cancelar coletas
              document.querySelectorAll(".btn-cancelar").forEach(button => {
                  button.addEventListener("click", cancelarColeta);
              });
          } else {
              alert("Erro ao carregar coletas.");
              console.error(coletas);
          }
      } catch (error) {
          console.error("Erro ao carregar coletas:", error);
      }
  }

  // Função para atualizar o status de uma coleta
  async function atualizarStatus(event) {
      const coletaID = event.target.getAttribute("data-id");
      const novoStatus = event.target.value;

      try {
          const response = await fetch(`http://127.0.0.1:5000/api/admin/coleta/${coletaID}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ status: novoStatus })
          });

          if (response.ok) {
              alert("Status atualizado com sucesso!");
          } else {
              alert("Erro ao atualizar status.");
          }
      } catch (error) {
          console.error("Erro ao atualizar status:", error);
      }
  }

  // Função para cancelar uma coleta
  async function cancelarColeta(event) {
      const coletaID = event.target.getAttribute("data-id");

      if (confirm("Tem certeza de que deseja cancelar este agendamento?")) {
          try {
              const response = await fetch(`http://127.0.0.1:5000/api/admin/coleta/${coletaID}`, {
                  method: "DELETE"
              });

              if (response.ok) {
                  alert("Agendamento cancelado com sucesso!");
                  carregarColetas(); // Recarrega a lista
              } else {
                  alert("Erro ao cancelar agendamento.");
              }
          } catch (error) {
              console.error("Erro ao cancelar agendamento:", error);
          }
      }
  }

  // Evento de clique no botão de pesquisa
  document.getElementById("btnSearch").addEventListener("click", function () {
      const filtro = searchInput.value.trim();
      carregarColetas(filtro);
  });

  // Carrega todas as coletas ao iniciar a página
  carregarColetas();
});
