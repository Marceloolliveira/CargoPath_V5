document.addEventListener("DOMContentLoaded", function () {
    // Função para construir o endereço completo
    function construirEndereco(rua, numero, cep, cidade, estado) {
        return `${rua}, ${numero}, ${cep}, ${cidade} - ${estado}`;
    }

    // Função para calcular o frete usando a API do Google Maps
    async function calcularFrete() {
        // Variáveis de entrada para os campos de endereço
        const inputRemetenteRua = document.getElementById("remetenteRua");
        const inputRemetenteNumero = document.getElementById("remetenteNumero");
        const inputRemetenteCEP = document.getElementById("remetenteCEP");
        const inputRemetenteCidade = document.getElementById("remetenteCidade");
        const inputRemetenteEstado = document.getElementById("remetenteEstado");

        const inputDestinoRua = document.getElementById("destinoRua");
        const inputDestinoNumero = document.getElementById("destinoNumero");
        const inputDestinoCEP = document.getElementById("destinoCEP");
        const inputDestinoCidade = document.getElementById("destinoCidade");
        const inputDestinoEstado = document.getElementById("destinoEstado");

        const enderecoRemetente = construirEndereco(
            inputRemetenteRua.value,
            inputRemetenteNumero.value,
            inputRemetenteCEP.value,
            inputRemetenteCidade.value,
            inputRemetenteEstado.value
        );

        const enderecoDestinatario = construirEndereco(
            inputDestinoRua.value,
            inputDestinoNumero.value,
            inputDestinoCEP.value,
            inputDestinoCidade.value,
            inputDestinoEstado.value
        );

        const valorCarga = parseFloat(document.getElementById("valorCarga").value) || 0;

        return new Promise((resolve, reject) => {
            const service = new google.maps.DistanceMatrixService();
            service.getDistanceMatrix(
                {
                    origins: [enderecoRemetente],
                    destinations: [enderecoDestinatario],
                    travelMode: 'DRIVING'
                },
                function (response, status) {
                    if (status === 'OK') {
                        const distancia = response.rows[0].elements[0].distance.value / 1000; // Distância em km
                        const precoPorKm = 1.5;
                        const porcentagemCarga = 0.05;
                        const custoDistancia = distancia * precoPorKm;
                        const custoCarga = valorCarga * porcentagemCarga;
                        const valorFinalFrete = (custoDistancia + custoCarga).toFixed(2);

                        document.getElementById("resultado").innerHTML = `
                            <p>Distância: ${distancia.toFixed(2)} km</p>
                            <p>Valor Final do Frete: R$ ${valorFinalFrete}</p>
                        `;

                        resolve(valorFinalFrete);
                    } else {
                        console.error("Erro ao calcular a distância:", status);
                        alert("Erro ao calcular a cotação. Tente novamente.");
                        reject("Erro ao calcular a distância");
                    }
                }
            );
        });
    }

    // Função para confirmar e salvar todos os dados no banco de dados
    async function confirmarCotacao() {
        console.log("Botão Confirmar clicado");
        const usuarioID = localStorage.getItem("usuarioID");
        const descricaoPedido = document.getElementById("descricaoPedido").value;

        try {
            // Calcular o frete primeiro
            const valorFrete = await calcularFrete();

            // 1. Criação da Cotação
            const cotacaoResponse = await fetch("http://127.0.0.1:5000/api/cotacao", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    descricao: descricaoPedido,
                    status: "pendente",
                    user_id: usuarioID,
                    valor_frete: valorFrete
                })
            });

            const cotacaoData = await cotacaoResponse.json();

            if (!cotacaoResponse.ok) {
                alert("Erro ao criar cotação: " + cotacaoData.error);
                return;
            }

            // Salvar o ID da cotação no localStorage
            localStorage.setItem("cotacaoId", cotacaoData.cotacao_id);

            // 2. Criar Localizações para Remetente e Destino
            const remetente = {
                rua: document.getElementById("remetenteRua").value,
                numero: document.getElementById("remetenteNumero").value,
                cep: document.getElementById("remetenteCEP").value,
                cidade: document.getElementById("remetenteCidade").value,
                estado: document.getElementById("remetenteEstado").value,
                complemento: document.getElementById("remetenteComplemento").value,
                tipo: 1,
                cotacao_id: cotacaoData.cotacao_id
            };

            const destino = {
                rua: document.getElementById("destinoRua").value,
                numero: document.getElementById("destinoNumero").value,
                cep: document.getElementById("destinoCEP").value,
                cidade: document.getElementById("destinoCidade").value,
                estado: document.getElementById("destinoEstado").value,
                complemento: document.getElementById("destinoComplemento").value,
                tipo: 2,
                cotacao_id: cotacaoData.cotacao_id
            };

            await Promise.all([
                fetch("http://127.0.0.1:5000/api/localizacao", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(remetente)
                }),
                fetch("http://127.0.0.1:5000/api/localizacao", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(destino)
                })
            ]);

            alert("Cotação criada com sucesso!");
            window.location.href = "/src/app/pages/price/resume/resume.html";
        } catch (error) {
            console.error("Erro ao salvar dados da cotação:", error);
            alert("Erro ao salvar dados da cotação. Verifique o console.");
        }
    }

    // Evento de clique no botão Confirmar para calcular e salvar cotação
    document.getElementById("btnConfirmar").addEventListener("click", confirmarCotacao);
});
