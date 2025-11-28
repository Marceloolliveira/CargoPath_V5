document.getElementById("btn-cadastrar").addEventListener("click", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const name = document.getElementById("name").value;
  const telefone = document.getElementById("telefone").value;
  const cpf = document.getElementById("cpf").value;

  try {
      const response = await fetch("http://127.0.0.1:5000/api/register", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ email, password, name,telefone, cpf })
      });

      if (response.ok) {
          const data = await response.json();
          alert("Cadastro realizado com sucesso!");
          window.location.href = "http://127.0.0.1:5501/login.html";
      } else {
          const error = await response.json();
          alert(error.error || "Erro no cadastro");
      }
  } catch (error) {
      console.error("Erro:", error);
      alert("Erro ao conectar com o servidor");
  }
});
