// Popular modal eliminar usuario con información del usuario al abrir el modal
const clientNameSpan = document.getElementById("nombre-eliminar")
const clientMailSpan = document.getElementById("mail-eliminar")
const deleteClientModal = document.getElementById("delete-client-modal")
const deleteClientBtn = document.getElementById("delete-cliente-btn")

deleteClientModal.addEventListener('show.bs.modal', () => {
    setTimeout(() => {
        var row = table.getRow(idActualizado)
        clientNameSpan.innerHTML = row.getData().first_name + " " + row.getData().last_name
        clientMailSpan.innerHTML = row.getData().email
    }, 1)
})

btnEliminarUsuario.addEventListener("click", () => {
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