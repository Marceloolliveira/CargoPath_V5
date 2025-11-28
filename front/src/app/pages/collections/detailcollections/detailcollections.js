document.addEventListener("DOMContentLoaded", async function () {
  const cotacaoId = localStorage.getItem("cotacaoId");
  if (!cotacaoId) {
      alert("ID da coleta não encontrado.");
      return;
  }

  try {
      const response = await fetch(`http://127.0.0.1:5000/api/cotacao/resumo/${cotacaoId}`);
      const data = await response.json();

      if (!response.ok) {
          throw new Error(data.error || "Erro ao carregar os detalhes da coleta.");
      }

      document.querySelector(".IdCotacao").textContent = `ID da Coleta: ${data.cotacao_id}`;
      document.querySelector(".status").textContent = `Status: ${data.status || "Não informado"}`;
      document.getElementById("dataAgendamento").value = data.data_agendamento || "Não informada";

      preencherDados("remetente", data.remetente);
      preencherDados("destino", data.destino);

      document.getElementById("valorCarga").value = data.carga.valor || "0.00";
      document.getElementById("pesoCarga").value = data.carga.peso || "0";
      document.getElementById("volumesCarga").value = data.carga.volumes || "0";

      const cubagemRow = `
          <tr>
              <td>${data.cubagem.id || "N/A"}</td>
              <td>${data.cubagem.altura || "0"}</td>
              <td>${data.cubagem.largura || "0"}</td>
              <td>${data.cubagem.comprimento || "0"}</td>
              <td>${data.cubagem.quantidade || "0"}</td>
          </tr>`;
      document.getElementById("cubagemBody").innerHTML = cubagemRow;

      const embalagemSelecionada = `
          Caixa: ${data.embalagem.caixa || "Não"}<br>
          Palet: ${data.embalagem.palet || "Não"}<br>
          Grade: ${data.embalagem.grade || "Não"}
      `;
      document.getElementById("embalagemSelecionada").innerHTML = `Embalagem Selecionada: <span>${embalagemSelecionada}</span>`;
  } catch (error) {
      console.error("Erro ao carregar os detalhes da coleta:", error);
  }
});

function preencherDados(tipo, dados) {
  document.getElementById(`${tipo}Rua`).value = dados.rua || "";
  document.getElementById(`${tipo}Numero`).value = dados.numero || "";
  document.getElementById(`${tipo}CEP`).value = dados.cep || "";
  document.getElementById(`${tipo}Cidade`).value = dados.cidade || "";
  document.getElementById(`${tipo}Estado`).value = dados.estado || "";
  document.getElementById(`${tipo}Bairro`).value = dados.bairro || "";
  document.getElementById(`${tipo}Complemento`).value = dados.complemento || "";
}

document.getElementById("btnPagar").addEventListener("click", function () {// Redirecionar para a tela de pagamento
    window.location.href = "/src/app/pages/price/resume/resume.html";
})