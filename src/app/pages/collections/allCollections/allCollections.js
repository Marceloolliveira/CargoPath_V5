document.addEventListener("DOMContentLoaded", function () {
  const userID = localStorage.getItem("usuarioID");

  if (!userID) {
      alert("Usuário não encontrado! Retornando para a página de login.");
      window.location.href = "../../login/login.html";
      return;
  }

  // Exibir nome do usuário
  document.getElementById("nomeUsuario").innerText = localStorage.getItem("usuarioNome");

  // Função para carregar coletas em andamento
  async function carregarColetas() {
      try {
          const response = await fetch(`http://127.0.0.1:5000/api/coletas?user_id=${userID}&status=andamento`);
          const coletas = await response.json();

          if (response.ok) {
              const listaColetas = document.getElementById("listaColetas");
              listaColetas.innerHTML = ""; // Limpa conteúdo anterior

              coletas.forEach(coleta => {
                  const divColeta = document.createElement("div");
                  divColeta.classList.add("coleta-item");
                  divColeta.innerHTML = `
                      <h3>ID da Coleta: ${coleta.coleta_id}</h3>
                      <p>Status: ${coleta.status}</p>
                      <p>Data de Agendamento: ${new Date(coleta.data_agendamento).toLocaleDateString()}</p>
                      <button class="btn btn-detalhar" onclick="detalharColeta(${coleta.coleta_id})">Ver Detalhes</button>
                  `;
                  listaColetas.appendChild(divColeta);
              });
          } else {
              console.error("Erro ao carregar coletas:", coletas);
              alert("Erro ao carregar coletas.");
          }
      } catch (error) {
          console.error("Erro ao carregar coletas:", error);
      }
  }

  // Função para redirecionar para os detalhes de uma coleta
  function detalharColeta(coletaID) {
      localStorage.setItem("coletaID", coletaID);
      window.location.href = "detalhes.html"; // Página de detalhes
  }

  // Carregar as coletas ao iniciar a página
  carregarColetas();
});
