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
