/* Alterna entre mostrar e esconder o conteúdo do dropdown */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
    }

    function toggleEtiquetas() {
    document.getElementById("etiquetasDropdown").classList.toggle("show");
}

// Fecha o dropdown se o usuário clicar fora dele
window.onclick = function(event) {
if (!event.target.matches('.dropdown-text')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
    }
    }
}
}