document.addEventListener("DOMContentLoaded", function () {
  const cotacaoID = localStorage.getItem("cotacaoID");
  const nomeUsuario = localStorage.getItem("usuarioNome");
  const valorFinalFrete = localStorage.getItem("valorFinalFrete");

  if (!cotacaoID || !valorFinalFrete) {
      alert("Dados da cotação não encontrados! Retornando à página de cotações.");
      window.location.href = "../../price/price.html";
      return;
  }

  document.getElementById("nomeUsuario").innerText = nomeUsuario;
  document.getElementById("resultado").insertAdjacentHTML(
      "afterbegin",
      `<h3>Valor Final do Frete: R$ ${valorFinalFrete}</h3>`
  );

  async function carregarDadosCotacao() {
      try {
          const cotacaoResponse = await fetch(`http://127.0.0.1:5000/api/cotacao/${cotacaoID}`);
          const cotacao = await cotacaoResponse.json();

          if (cotacaoResponse.ok) {
              document.getElementById("remetenteRua").value = cotacao.remetente.rua;
              document.getElementById("destinoRua").value = cotacao.destino.rua;
              document.getElementById("valorCarga").value = cotacao.carga.valor;
              document.getElementById("pesoCarga").value = cotacao.carga.peso;
              document.getElementById("volumesCarga").value = cotacao.carga.volumes;
          } else {
              alert("Erro ao carregar dados da cotação.");
              console.error(cotacao);
          }
      } catch (error) {
          console.error("Erro ao carregar dados da cotação:", error);
      }
  }

  async function processarPagamento() {
      try {
          const response = await fetch("http://127.0.0.1:5000/api/mercado_pago", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                  cotacao_id: cotacaoID,
                  valor: valorFinalFrete
              })
          });

          if (response.ok) {
              const pagamento = await response.json();
              alert(`Pagamento realizado com sucesso! Link: ${pagamento.payment_link}`);
              window.open(pagamento.payment_link, "_blank");
          } else {
              const error = await response.json();
              alert("Erro ao processar pagamento: " + error.message);
          }
      } catch (error) {
          console.error("Erro ao processar pagamento:", error);
          alert("Erro ao processar pagamento.");
      }
  }

  document.getElementById("btnPagar").addEventListener("click", processarPagamento);

  document.getElementById("btnNovaCotacao").addEventListener("click", function () {
      if (confirm("Tem certeza de que deseja cancelar?")) {
          window.location.href = "../../price/price.html";
      }
  });

  carregarDadosCotacao();
});
