// Se intercambia el modo del userModal para agregar o editar un archivo cambiando atributos y valores
var btnsEditar = document.getElementsByClassName("btn-editar-usuario")
var modalImgTitle = document.getElementById("modal-img-title")
var modalTitle = document.getElementById("modal-title")
var userForm = document.getElementById("user-form")
var btnSubmitUserForm = document.getElementById("btn-submit-form")

document.getElementById("btn-agregar-usuario").addEventListener("click", function () {
    toggleMode("agregar")
})


for (var i = 0; i < btnsEditar.length; i++) {
    btnsEditar[i].addEventListener('click', function(){
        toggleMode("editar")
    })
}


function toggleMode(mode){
    if (mode == "agregar"){
        modalImgTitle.setAttribute("src", imgAgregarUsuario)
        modalTitle.innerHTML = "Agregar un usuario"
        userForm.setAttribute("action", "/create_user")
        btnSubmitUserForm.innerHTML = "Agregar un usuario"
    } else if (mode == "editar"){
        modalImgTitle.setAttribute("src", imgEditarUsuario)
        modalTitle.innerHTML = "Editar un usuario"
        userForm.setAttribute("action", "/edit")
        btnSubmitUserForm.innerHTML = "Editar un usuario"
    }
}
