document.addEventListener("DOMContentLoaded", function () {
  const cotacaoId = localStorage.getItem("cotacaoId");
  const valorFinalFrete = localStorage.getItem("valorFinalFrete");
  const destinatario = localStorage.getItem("destinatario");
  const dataAgendamento = localStorage.getItem("dataAgendamento");

  if (!cotacaoId || !valorFinalFrete) {
    console.error("Cotação ou valor do frete não encontrado no localStorage.");
    alert("Erro ao carregar os dados do pagamento.");
    return;
  }

  // Atualizar a página com os dados recuperados
  document.getElementById("cotacaoId").textContent = cotacaoId;
  document.getElementById("valorPagamento").textContent = parseFloat(valorFinalFrete).toFixed(2);
  document.getElementById("destinatarioNome").textContent = destinatario || "Não informado";
  document.getElementById("dataAgendamento").textContent = dataAgendamento || "Não informado";

  const mp = new MercadoPago("TEST-f5a1b082-2c41-45c9-9bfe-668172eea53d");
  const bricksBuilder = mp.bricks();

  // Função para buscar o preferenceId no backend
  async function fetchPreferenceId() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/payment/create_preference", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cotacaoId: cotacaoId,
          amount: parseFloat(valorFinalFrete),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Erro ao criar a preferência de pagamento.");
      }

      const data = await response.json();
      console.log("Preference ID recebido:", data.preferenceId);

      return data.preferenceId;
    } catch (error) {
      console.error("Erro ao buscar o preferenceId:", error);
      throw error;
    }
  }

  // Função para carregar o Payment Brick
  async function loadPaymentBrick() {
    try {
      const preferenceId = await fetchPreferenceId();

      mp.bricks().create("wallet", "wallet_container", {
        initialization: {
          amount: parseFloat(valorFinalFrete),
          preferenceId: preferenceId,
        },
        paymentMethods: {
          ticket: false, // Desabilita boletos (opcional)
          bank_transfer: false, // Desabilita transferências (opcional)
        },
        callbacks: {
          onReady: () => {
            console.log("Payment Brick carregado com sucesso!");
          },
          onSubmit: (formData) => {
            console.log("Dados enviados para o pagamento:", formData);     
          },
          onError: (error) => {
            console.error("Erro ao carregar o Payment Brick:", error);
          },
        },
      });
    } catch (error) {
      console.error("Erro ao inicializar o Payment Brick:", error);
    }
  }

  console.log("Iniciando Payment Brick com os seguintes dados:");
  console.log("Amount:", parseFloat(valorFinalFrete));

  loadPaymentBrick();
});


document.getElementById("voltarResumo").addEventListener("click", function () {
  localStorage.removeItem("cotacaoId");
  localStorage.removeItem("valorFinalFrete");
  localStorage.removeItem("destinatario");
  localStorage.removeItem("dataAgendamento");
  window.location.href = "/src/app/pages/price/price.html";
});
