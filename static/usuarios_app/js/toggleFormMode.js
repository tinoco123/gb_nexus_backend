// Se intercambia el modo del userModal para agregar o editar un archivo cambiando atributos y valores
var btnsEditar = document.getElementsByClassName("editar-usuario")
var modalImgTitle = document.getElementById("modal-img-title")
var modalTitle = document.getElementById("modal-title")
var userForm = document.getElementById("user-form")
var btnSubmitUserForm = document.getElementById("btn-submit-form")
var idActualizado = 0

table.on("rowClick", function (e, row) {
    idActualizado = row.getData().id
});

document.getElementById("btn-agregar-usuario").addEventListener("click", function () {
    toggleMode("agregar")
})

table.on("dataProcessed", function () {
    setEventListnerToEditButtons()
});

table.on("pageLoaded", function (pageno) {
    setEventListnerToEditButtons()
});


function setEventListnerToEditButtons() {
    for (var i = 0; i < btnsEditar.length; i++) {
        btnsEditar[i].addEventListener('click', function () {
            toggleMode("editar")
        })
    }
}


function toggleMode(mode) {
    if (mode == "agregar") {
        modalMode = "agregar"

        modalImgTitle.setAttribute("src", imgAgregarUsuario)
        modalTitle.innerHTML = "Agregar un usuario"
        btnSubmitUserForm.innerHTML = "Agregar un usuario"
    } else if (mode == "editar") {
        modalMode = "editar"

        modalImgTitle.setAttribute("src", imgEditarUsuario)
        modalTitle.innerHTML = "Editar un usuario"
        btnSubmitUserForm.innerHTML = "Editar un usuario"
    }
}


// Borrar datos del formulario al cerrar el modal
const userModal = document.getElementById('userModal')
userModal.addEventListener('hide.bs.modal', event => {
    userForm = document.getElementById("user-form")
    userForm.reset()
})