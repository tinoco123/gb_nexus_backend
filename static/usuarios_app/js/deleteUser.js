// Popular modal eliminar usuario con información del usuario al abrir el modal
const clientNameSpan = document.getElementById("nombre-eliminar")
const clientMailSpan = document.getElementById("mail-eliminar")
const deleteUserModal = document.getElementById("delete-user-modal")
const deleteUserBtn = document.getElementById("delete-user-btn")

deleteUserModal.addEventListener('show.bs.modal', () => {
    setTimeout(() => {
        var row = table.getRow(idActualizado)
        clientNameSpan.innerHTML = row.getData().first_name + " " + row.getData().last_name
        clientMailSpan.innerHTML = row.getData().email
    }, 1)
})

deleteUserBtn.addEventListener("click", () => {
    fetch("/users/delete/" + idActualizado, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/users/";
            }
            else if (response.status >= 400 || response.status < 500) {
                response.json()
                    .then(errors => {
                        showNotifications(response.status, "Error de usuario: Hubo un error al procesar tu solicitud")
                        console.error(errors);
                    })
                    .catch((error) => {
                        showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
                        console.error(error)
                    })
            }
        })
        .catch((error) => {
            showNotifications(500, "Error del servidor: El servidor falló al procesar tu solicitud")
            console.error(error)
        })
})
