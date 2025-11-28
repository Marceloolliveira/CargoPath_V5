document.addEventListener("DOMContentLoaded", function () {
    function construirEndereco(rua, numero, cep, cidade, estado) {
        return `${rua}, ${numero}, ${cep}, ${cidade} - ${estado}`;
    }

    flatpickr("#dataAgendamento", {
        altInput: true, 
        altFormat: "F j, Y", 
        dateFormat: "Y-m-d", 
        minDate: "today",
        locale: "pt",
    });

    function waitForGoogleMaps(timeout = 10000) {
        return new Promise((resolve, reject) => {
            if (window.google && window.google.maps) return resolve();
            const intervalMs = 100;
            let waited = 0;
            const iv = setInterval(() => {
                if (window.google && window.google.maps) {
                    clearInterval(iv);
                    resolve();
                }
                waited += intervalMs;
                if (waited >= timeout) {
                    clearInterval(iv);
                    reject(new Error('Google Maps API não carregou dentro do tempo limite'));
                }
            }, intervalMs);
        });
    }

    async function fallbackDistanceUsingNominatim(originAddress, destAddress) {
        console.warn('Usando fallback Nominatim para calcular distância');
        const encode = (s) => encodeURIComponent(s);
        const urlFor = (q) => `https://nominatim.openstreetmap.org/search?format=json&q=${encode(q)}`;

        try {
            const [oResp, dResp] = await Promise.all([
                fetch(urlFor(originAddress), { headers: { 'User-Agent': 'CargoPathApp/1.0' } }),
                fetch(urlFor(destAddress), { headers: { 'User-Agent': 'CargoPathApp/1.0' } }),
            ]);
            const [oJson, dJson] = await Promise.all([oResp.json(), dResp.json()]);
            if (!oJson.length || !dJson.length) throw new Error('Não foi possível geocodificar um dos endereços via Nominatim');

            const oLat = parseFloat(oJson[0].lat);
            const oLon = parseFloat(oJson[0].lon);
            const dLat = parseFloat(dJson[0].lat);
            const dLon = parseFloat(dJson[0].lon);

            const toRad = (v) => (v * Math.PI) / 180;
            const R = 6371;
            const dLatR = toRad(dLat - oLat);
            const dLonR = toRad(dLon - oLon);
            const a = Math.sin(dLatR / 2) * Math.sin(dLatR / 2) + Math.cos(toRad(oLat)) * Math.cos(toRad(dLat)) * Math.sin(dLonR / 2) * Math.sin(dLonR / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            const distanciaKm = R * c;
            return distanciaKm;
        } catch (err) {
            console.error('Fallback Nominatim falhou:', err);
            throw err;
        }
    }

    async function calcularFrete() {
        let googleAvailable = true;
        try {
            await waitForGoogleMaps(3000);
        } catch (err) {
            googleAvailable = false;
            console.warn('Google Maps API não disponível, usaremos fallback:', err);
        }
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

        if (googleAvailable && window.google && window.google.maps) {
            return new Promise((resolve, reject) => {
                const service = new google.maps.DistanceMatrixService();
                service.getDistanceMatrix(
                    {
                        origins: [enderecoRemetente],
                        destinations: [enderecoDestinatario],
                        travelMode: "DRIVING",
                    },
                    async function (response, status) {
                        if (status === "OK") {
                            try {
                                const distancia = response.rows[0].elements[0].distance.value / 1000;
                                const precoPorKm = 1.5;
                                const porcentagemCarga = 0.05;
                                const custoDistancia = distancia * precoPorKm;
                                const custoCarga = valorCarga * porcentagemCarga;
                                const valorFinalFrete = (custoDistancia + custoCarga).toFixed(2);
                                resolve(valorFinalFrete);
                            } catch (err) {
                                console.error('Erro ao processar resposta do Google Maps:', err);
                                try {
                                    const distanciaKm = await fallbackDistanceUsingNominatim(enderecoRemetente, enderecoDestinatario);
                                    const precoPorKm = 1.5;
                                    const porcentagemCarga = 0.05;
                                    const custoDistancia = distanciaKm * precoPorKm;
                                    const custoCarga = valorCarga * porcentagemCarga;
                                    const valorFinalFrete = (custoDistancia + custoCarga).toFixed(2);
                                    resolve(valorFinalFrete);
                                } catch (fbErr) {
                                    reject(fbErr);
                                }
                            }
                        } else {
                            console.warn('Google DistanceMatrix retornou status:', status, 'tentando fallback');
                            try {
                                const distanciaKm = await fallbackDistanceUsingNominatim(enderecoRemetente, enderecoDestinatario);
                                const precoPorKm = 1.5;
                                const porcentagemCarga = 0.05;
                                const custoDistancia = distanciaKm * precoPorKm;
                                const custoCarga = valorCarga * porcentagemCarga;
                                const valorFinalFrete = (custoDistancia + custoCarga).toFixed(2);
                                resolve(valorFinalFrete);
                            } catch (fbErr) {
                                reject(fbErr);
                            }
                        }
                    }
                );
            });
        } else {
            try {
                const distanciaKm = await fallbackDistanceUsingNominatim(enderecoRemetente, enderecoDestinatario);
                const precoPorKm = 1.5;
                const porcentagemCarga = 0.05;
                const custoDistancia = distanciaKm * precoPorKm;
                const custoCarga = valorCarga * porcentagemCarga;
                const valorFinalFrete = (custoDistancia + custoCarga).toFixed(2);
                return valorFinalFrete;
            } catch (err) {
                console.error('Não foi possível calcular distância (fallback também falhou):', err);
                throw err;
            }
        }
    }

    async function confirmarCotacao() {
        console.log('confirmarCotacao: iniciando');
        const btnConfirmar = document.getElementById("btnConfirmar");
        if (btnConfirmar) btnConfirmar.disabled = true;

        const usuarioID = localStorage.getItem("usuarioID");
        console.log('usuarioID from localStorage:', usuarioID);
        if (!usuarioID) {
            alert('Usuário não autenticado. Faça login antes de criar uma cotação.');
            if (btnConfirmar) btnConfirmar.disabled = false;
            return;
        }
        const descricaoPedido = document.getElementById("descricaoPedido").value;
        const dataAgendamento = document.getElementById("dataAgendamento").value;

        try {
            console.log('confirmarCotacao: chamando calcularFrete()');
            const valorFrete = await calcularFrete();
            console.log('confirmarCotacao: valorFrete calculado =', valorFrete);

            const cotacaoResponse = await fetch("http://127.0.0.1:5000/api/cotacao/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    descricao: descricaoPedido,
                    status: "pendente",
                    user_id: usuarioID,
                    valor_frete: valorFrete,
                    data_agendamento: dataAgendamento,
                }),
            });

            const cotacaoData = await cotacaoResponse.json();
            if (!cotacaoResponse.ok) {
                console.error('confirmarCotacao: resposta com erro ao criar cotacao:', cotacaoData);
                alert("Erro ao criar cotação: " + (cotacaoData.error || JSON.stringify(cotacaoData)));
                if (btnConfirmar) btnConfirmar.disabled = false;
                return;
            }

            const cotacaoId = cotacaoData.cotacao_id;
            localStorage.setItem("cotacaoId", cotacaoId);

            const remetente = {
                rua: document.getElementById("remetenteRua").value,
                numero: document.getElementById("remetenteNumero").value,
                cep: document.getElementById("remetenteCEP").value,
                cidade: document.getElementById("remetenteCidade").value,
                estado: document.getElementById("remetenteEstado").value,
                complemento: document.getElementById("remetenteComplemento").value,
                tipo: 1,
                cotacao_id: cotacaoId,
            };

            const destino = {
                rua: document.getElementById("destinoRua").value,
                numero: document.getElementById("destinoNumero").value,
                cep: document.getElementById("destinoCEP").value,
                cidade: document.getElementById("destinoCidade").value,
                estado: document.getElementById("destinoEstado").value,
                complemento: document.getElementById("destinoComplemento").value,
                destinatario_nome: document.getElementById("destinatarioNome").value,
                tipo: 2,
                cotacao_id: cotacaoId,
            };

            await Promise.all([
                fetch("http://127.0.0.1:5000/api/localizacao", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(remetente),
                }),
                fetch("http://127.0.0.1:5000/api/localizacao", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(destino),
                }),
            ]);

            const cargaResponse = await fetch("http://127.0.0.1:5000/api/carga", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    valor: document.getElementById("valorCarga").value,
                    peso: document.getElementById("pesoCarga").value,
                    volumes: document.getElementById("volumesCarga").value,
                    cotacao_id: cotacaoId,
                }),
            });

            const cargaData = await cargaResponse.json();
            if (!cargaResponse.ok) {
                console.error("Erro ao criar carga:", cargaData.error);
                return;
            }

            const cubagemLinhas = document.querySelectorAll("#cubagemBody tr");
            for (const linha of cubagemLinhas) {
                const inputs = linha.querySelectorAll("input");
                await fetch("http://127.0.0.1:5000/api/cubagem", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        altura: inputs[0].value,
                        largura: inputs[1].value,
                        comprimento: inputs[2].value,
                        qtd: inputs[3].value,
                        carga_id: cargaData.carga_id,
                    }),
                });
            }

            const embalagemSelecionada = document.querySelector('input[name="embalagem"]:checked');
            if (embalagemSelecionada) {
                const embalagemResponse = await fetch("http://127.0.0.1:5000/api/embalagem", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        caixa: embalagemSelecionada.value === "caixa" ? "sim" : null,
                        palet: embalagemSelecionada.value === "palet" ? "sim" : null,
                        grade: embalagemSelecionada.value === "grade" ? "sim" : null,
                        cubagem_id: cargaData.carga_id,
                    }),
                });
                if (!embalagemResponse.ok) {
                    console.error("Erro ao criar embalagem:", await embalagemResponse.json());
                }
            } else {
                alert("Selecione uma embalagem antes de continuar.");
            }

            alert("Cotação criada com sucesso!");
            window.location.href = "/src/app/pages/price/resume/resume.html";
        } catch (error) {
            console.error("Erro ao salvar dados da cotação:", error);
            alert('Erro ao salvar dados da cotação. Veja o console para detalhes.');
        }
        finally {
            if (document.getElementById("btnConfirmar")) document.getElementById("btnConfirmar").disabled = false;
        }
    }

    document.getElementById("btnConfirmar").addEventListener("click", confirmarCotacao);
});
