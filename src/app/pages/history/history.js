document.addEventListener("DOMContentLoaded", function () {
  const userID = localStorage.getItem("usuarioID");

  if (!userID) {
      alert("Usuário não encontrado! Retornando para a página de login.");
      window.location.href = "../../login/login.html";
      return;
  }

  // Exibir o nome do usuário
  document.getElementById("nomeUsuario").innerText = localStorage.getItem("usuarioNome");

  // Função para carregar histórico de cotações
  async function carregarHistorico() {
      try {
          const response = await fetch(`http://127.0.0.1:5000/api/cotacoes?user_id=${userID}`);
          const historico = await response.json();

          if (response.ok) {
              const historicoContainer = document.getElementById("historicoCotacoes");
              historico.forEach(cotacao => {
                  const divCotacao = document.createElement("div");
                  divCotacao.classList.add("cotacao-item");
                  divCotacao.innerHTML = `
                      <h3>ID da Cotação: ${cotacao.cotacao_id}</h3>
                      <p>Descrição: ${cotacao.descricao}</p>
                      <p>Status: ${cotacao.status}</p>
                      <p>Valor do Frete: R$ ${cotacao.valor_frete}</p>
                      <p>Data: ${new Date(cotacao.created_at).toLocaleString()}</p>
                      <button class="btn btn-primary" onclick="detalharCotacao(${cotacao.cotacao_id})">Ver Detalhes</button>
                  `;
                  historicoContainer.appendChild(divCotacao);
              });
          } else {
              alert("Erro ao carregar o histórico de cotações.");
              console.error(historico);
          }
      } catch (error) {
          console.error("Erro ao carregar histórico:", error);
          alert("Erro ao carregar o histórico. Verifique o console.");
      }
  }

  // Função para redirecionar para detalhes de uma cotação específica
  function detalharCotacao(cotacaoID) {
      localStorage.setItem("cotacaoID", cotacaoID);
      window.location.href = "../resume/resume.html";
  }

  // Carregar histórico ao iniciar a página
  carregarHistorico();
});
