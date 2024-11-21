// common.js
document.addEventListener("DOMContentLoaded", function () {
  // Expandir e recolher o menu lateral
  const menuExpand = document.querySelector("#btn-exp");
  const menuSide = document.querySelector(".menu-lateral");

  if (menuExpand && menuSide) {
      menuExpand.addEventListener("click", function () {
          menuSide.classList.toggle("expandir");
      });
  }
});

document.getElementById("sair").addEventListener("click", function () {
  localStorage.clear();
  window.location.href = "http://127.0.0.1:5501/login.html";
});