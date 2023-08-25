const deleteKeywordModal = document.getElementById("delete-keyword-modal")
const deleteKeywordBtn = document.getElementById("delete-keyword-btn")
const idEliminar = document.getElementById("id-eliminar")
const keyword = document.getElementById("keyword-eliminar")

deleteKeywordModal.addEventListener("show.bs.modal", () => {
    setTimeout(() => {
        var row = table.getRow(idActualizado)
        var first_keyword = row.getData().first_keyword
        var second_keyword = row.getData().second_keyword
        idEliminar.innerHTML = idActualizado
        if (second_keyword == null) {
            keyword.innerHTML = first_keyword
        } else {
            keyword.innerHTML = first_keyword + " | " + second_keyword
        }
    }, 1)
})

deleteKeywordBtn.addEventListener("click", () => {
    fetch("/keywords/delete/" + idActualizado, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/keywords";
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