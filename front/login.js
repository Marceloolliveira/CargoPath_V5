document.getElementById("btn-login").addEventListener("click", async (e) => {
    e.preventDefault();
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    try {
        const response = await fetch("http://127.0.0.1:5000/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });
  
        if (response.ok) {
            const data = await response.json();

            localStorage.setItem("token", data.token);
            localStorage.setItem("usuarioID", data.user_id);
            localStorage.setItem("usuarioNome", data.name);
            
            alert("Login bem-sucedido!");
            window.location.href = "src/app/pages/dashboard/dashboard.html";
        } else {
            const error = await response.json();
            alert(error.message || "Erro no login");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao conectar com o servidor");
    }
});
