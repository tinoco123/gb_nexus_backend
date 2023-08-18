// Al abrir el modal prellenar el formulario con los datos del usuario seleccionado
const editClientModal = document.getElementById('edit-client-modal')
editClientModal.addEventListener('show.bs.modal', event => {
    setTimeout(() => getClientById(idActualizado), 1)
})

function getClientById(user_id) {
    fetch("/clients/get/" + user_id, {
        method: "GET"
    })
        .then(response => {
            response.json()
                .then(data => {
                    if (response.ok) {
                        var editClientForm = document.getElementById("edit-client-form")
                        fillFormWithData(data, editClientForm)
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

const editClientForm = document.getElementById("edit-client-form").addEventListener("submit", event => {
    event.preventDefault();
    var formData = new FormData(event.target);
    editClient(formData, idActualizado)
})

function editClient(formData, user_id) {
    fetch("/clients/edit/" + user_id, {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/clients"
            } else if (response.status >= 400 || response.status < 500) {
                response.json()
                    .then(form_errors => {
                        setErrorsInForm(form_errors)
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