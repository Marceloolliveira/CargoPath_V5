document.addEventListener("DOMContentLoaded", function () {
    const userId = localStorage.getItem("usuarioID");

    if (!userId) {
        alert("Usuário não identificado. Faça login novamente.");
        window.location.href = "/login.html";
        return;
    }

    // Atualiza o nome do usuário no dashboard
    const usuarioNome = localStorage.getItem("usuarioNome");
    if (usuarioNome) {
        document.getElementById("nomeDashboard").innerText = `Olá ${usuarioNome}, seja bem-vindo!`;
    }

    console.log("Dashboard carregado!");

// Selecionar item no menu lateral
var MenuItem = document.querySelectorAll('.item-menu');

function SelectLink(){
    MenuItem.forEach((item) =>
        item.classList.remove('ativo')
    );
    this.classList.add('ativo');
}

MenuItem.forEach((item) =>
    item.addEventListener('click', SelectLink)
);

// Expandir menu
var MenuExpand = document.querySelector('#btn-exp');
var MenuSide = document.querySelector('.menu-lateral');

MenuExpand.addEventListener('click', function() {
    MenuSide.classList.toggle('expandir');
});

    const updateCard = (selector, value) => {
        const element = document.querySelector(selector);

        if (!element) {
            console.error(`Elemento com seletor ${selector} não encontrado.`);
            return;
        }

        const countElement = element.querySelector(".count") || element;
        const finalValue = parseInt(value, 10);
        let current = 0;

        const interval = setInterval(() => {
            countElement.textContent = current;
            if (current >= finalValue) {
                clearInterval(interval);
            }
            current += Math.ceil(finalValue / 50);
        }, 30);
    };

    const updateChart = (chart, value) => {
        chart.data.datasets[0].data = [value, 100 - value];
        chart.update();
    };

    let totalChart, completedChart, cancelledChart;

    const initializeCharts = () => {
        const ctxTotal = document.getElementById("totalChart").getContext("2d");
        const ctxCompleted = document.getElementById("completedChart").getContext("2d");
        const ctxCancelled = document.getElementById("cancelledChart").getContext("2d");

        totalChart = new Chart(ctxTotal, {
            type: "doughnut",
            data: {
                labels: ["Total", "Restante"],
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ["#414bb2", "#e0e0e0"]
                }]
            },
            options: { responsive: true }
        });

        completedChart = new Chart(ctxCompleted, {
            type: "doughnut",
            data: {
                labels: ["Finalizadas", "Restante"],
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ["#27ae60", "#e0e0e0"]
                }]
            },
            options: { responsive: true }
        });

        cancelledChart = new Chart(ctxCancelled, {
            type: "doughnut",
            data: {
                labels: ["Canceladas", "Restante"],
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ["#e74c3c", "#e0e0e0"]
                }]
            },
            options: { responsive: true }
        });
    };

    async function fetchDashboardData(startDate = null, endDate = null) {
        try {
            const queryParams = new URLSearchParams();
            queryParams.append("user_id", userId);
            if (startDate) queryParams.append("startDate", startDate);
            if (endDate) queryParams.append("endDate", endDate);

            const response = await fetch(`http://127.0.0.1:5000/api/dashboard/?${queryParams}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Erro ao carregar o resumo.");
            }

            updateCard("#pendingCount", data.pending);

            document.getElementById("totalValue").textContent = data.total;
            document.getElementById("completedValue").textContent = data.completed;
            document.getElementById("cancelledValue").textContent = data.cancelled;

            updateChart(totalChart, data.total);
            updateChart(completedChart, data.completed);
            updateChart(cancelledChart, data.cancelled);
        } catch (error) {
            console.error("Erro ao carregar o resumo do dashboard:", error);
            alert("Erro ao carregar o resumo do dashboard.");
        }
    }

    document.getElementById("applyFilters").addEventListener("click", () => {
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        fetchDashboardData(startDate, endDate);
    });

    initializeCharts();
    fetchDashboardData();

    document.getElementById("sair").addEventListener("click", function () {
        localStorage.clear();
        window.location.href = "/login.html";
    });
});
