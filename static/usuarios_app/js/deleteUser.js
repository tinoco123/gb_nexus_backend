// Popular modal eliminar usuario con información del usuario al abrir el modal
const spanNombreUsuario = document.getElementById("nombre-eliminar")
const spanMailUsuario = document.getElementById("mail-eliminar")
const modalEliminarUsuario = document.getElementById("eliminarUsuarioModal")
const btnEliminarUsuario = document.getElementById("eliminar-usuario-btn")

modalEliminarUsuario.addEventListener('shown.bs.modal', event => {
    var row = table.getRow(rowIndex)
    var nombreUsuario = row.getData().first_name
    var mailUsuario = row.getData().email
    spanNombreUsuario.innerHTML = nombreUsuario
    spanMailUsuario.innerHTML = mailUsuario
})

btnEliminarUsuario.addEventListener("click", function () {
    fetch("/users/delete/" + idActualizado, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/clients";
            }
            else if (response.status >= 400 || response.status < 500) {
                response.json()
                    .then(errors => {
                        showNotifications(response.status, "Error de usuario: Hubo un error al procesar tu solicitud")
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
