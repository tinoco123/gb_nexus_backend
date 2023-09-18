// Al abrir el modal prellenar el formulario con los datos del usuario seleccionado
const editUserModal = document.getElementById('edit-user-modal')
editUserModal.addEventListener('show.bs.modal', event => {
    setTimeout(() => getUserById(idActualizado), 1)
})

function getUserById(user_id) {
    fetch("/users/get/" + user_id, {
        method: "GET"
    })
        .then(response => {
            response.json()
                .then(data => {
                    if (response.ok) {
                        var editUserForm = document.getElementById("edit-user-form")
                        fillFormWithData(data, editUserForm)
                    }
                    else if (response.status >= 400 && response.status < 500) {
                        showNotifications(response.status, "Error de usuario: Tu solicitud no se pudo procesar correctamente")
                    }
                })
                .catch(error => {
                    showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
                    console.error(error)
                })
        })
        .catch(error => {
            showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
            console.error(error)
        })
}

const editUserForm = document.getElementById("edit-user-form").addEventListener("submit", event => {
    event.preventDefault();
    var formData = new FormData(event.target);
    editUser(formData, idActualizado)
})

function editUser(formData, user_id) {
    fetch("/users/edit/" + user_id, {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/users"
            } else if (response.status >= 400 && response.status < 500) {
                response.json()
                    .then(form_errors => {
                        setErrorsInForm(form_errors, "error_edit_")
                        showNotifications(response.status, "Error de usuario: Existen errores en tu formulario")
                    })
                    .catch(() => {
                        showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
                    })
            }
        })
        .catch(error => {
            showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
            console.error(error)
        })
}