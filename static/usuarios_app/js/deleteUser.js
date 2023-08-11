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
        .then(function (response) {
            if (response.ok) {
                window.location.href = urlUsers;
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
})
