// Se intercambia el modo del userModal para agregar o editar un archivo cambiando atributos y valores
var modalImgTitle = document.getElementById("modal-img-title")
var modalTitle = document.getElementById("modal-title")
var userForm = document.getElementById("user-form")
var btnSubmitUserForm = document.getElementById("btn-submit-form")
var idActualizado = 0

// Habilitar por defecto el modo editar en el formulario
modalMode = "editar"
toggleMode(modalMode)

table.on("rowClick", function (e, row) {
    idActualizado = row.getData().id
});

document.getElementById("btn-agregar-usuario").addEventListener("click", function () {
    modalMode = "agregar"
    toggleMode(modalMode)
})

function toggleMode(mode) {
    if (mode == "agregar") {
        document.getElementById("id_password").setAttribute("required", "")
        modalImgTitle.setAttribute("src", imgAgregarUsuario)
        modalTitle.innerHTML = "Agregar un usuario"
        btnSubmitUserForm.innerHTML = "Agregar un usuario"
    } else if (mode == "editar") {
        modalImgTitle.setAttribute("src", imgEditarUsuario)
        modalTitle.innerHTML = "Editar un usuario"
        btnSubmitUserForm.innerHTML = "Editar un usuario"
        document.getElementById("id_password").removeAttribute("required")
    }
}

// Al cerrar el modal
const userModal = document.getElementById('userModal')
userModal.addEventListener('hide.bs.modal', event => {
    if (modalMode == "agregar"){
        modalMode = "editar"
        toggleMode(modalMode)
    }
    userForm.reset()
})

// Al abrir el modal
userModal.addEventListener('shown.bs.modal', event => {
    if (modalMode == "editar") {
        get_user(idActualizado)
            .then(function (userData) {
                fillForm(userData)
            })
            .catch(function (error) {
                console.error('Error al obtener el usuario:', error);
            });
    }

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
            throw error;
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