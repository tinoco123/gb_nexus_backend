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

table.on("pageLoaded", function () {
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

userModal.addEventListener('shown.bs.modal', event => {
    
    get_user(idActualizado)
        .then(function (userData) {
            fillForm(userData)
        })
        .catch(function (error) {
            console.error('Error al obtener el usuario:', error);
        });
})

function get_user(user_id) {
    return fetch("/users/get/" + user_id, {
        method: 'GET',
    })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('La respuesta no fue exitosa');
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
            throw error; // Puedes propagar el error o manejarlo de otra forma si lo deseas
        });
}

function fillForm(data) {
    userForm.id_first_name.value = data.first_name
    userForm.id_last_name.value = data.last_name
    userForm.id_email.value = data.email
    userForm.id_address.value = data.address
    userForm.id_company.value = data.company
    userForm.id_date_birth.value = data.date_birth
}