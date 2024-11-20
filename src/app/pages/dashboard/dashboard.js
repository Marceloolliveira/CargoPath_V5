
document.addEventListener('DOMContentLoaded', function() {
  

    console.log("Dashboard carregado!");
    
    var MenuItem = document.querySelectorAll('.item-menu');
    var appContent = document.getElementById('app');
    var IconHome = document.getElementById('inicio');
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
    });
    // -------------------------------------------------------------------------------
    // Recuperar nome de usuario

    const usuarioNome = localStorage.getItem("usuarioNome");

// Exibe o nome do usuário na página, se necessário
document.getElementById("nomeUsuario").innerText = usuarioNome;

//sair e limpar localStorage
document.getElementById("sair").addEventListener("click", function() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuarioID");
    localStorage.removeItem("usuarioNome");
    localStorage.removeItem("valorFinalFrete");
    localStorage.removeItem("cotacaoId");
    window.location.href = "../../../../login.html"; // Redireciona para a página de login
});



    
    
    
    
    
    
    