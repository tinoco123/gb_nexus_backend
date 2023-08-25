const editKeywordModal = document.getElementById("edit-keyword-modal")
editKeywordModal.addEventListener('show.bs.modal', event => {
    setTimeout(() => getKeywordById(idActualizado), 1)
})

function getKeywordById(keyword_id) {
    fetch("/keywords/get/" + keyword_id, {
        method: "GET"
    })
        .then(response => {
            response.json()
                .then(data => {
                    if (response.ok) {
                        var editKeywordForm = document.getElementById("edit-keyword-form")
                        fillFormWithData(data, editKeywordForm)
                    }
                    else if (response.status >= 400 && response.status < 500) {
                        showNotifications(response.status, "Error de usuario: No puedes ver una keyword de otro usuario")
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

const editKeywordForm = document.getElementById("edit-keyword-form").addEventListener("submit", event => {
    event.preventDefault();
    var formData = new FormData(event.target);
    editKeyword(formData, idActualizado)
})

function editKeyword(formData, keyword_id) {
    fetch("/keywords/edit/" + keyword_id, {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (response.ok) {
                window.location.href = "/keywords"
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

editKeywordModal.addEventListener("hidden.bs.modal", () => {
    document.getElementById("edit-keyword-form").reset()
})