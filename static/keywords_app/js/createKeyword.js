const createKeywordForm = document.getElementById("create-keyword-form")
createKeywordForm.addEventListener("submit", (event) => {
    event.preventDefault()
    var formData = new FormData(event.target)
    fetch("/keywords/create/", {
        method: "POST",
        body: formData
    })
        .then((response) => {
            if (response.ok) {
                window.location.href = "/keywords";
            }
            else if (response.status >= 400 || response.status < 500) {
                response.json()
                    .then((form_errors) => {
                        setErrorsInForm(form_errors)
                        showNotifications(response.status, "Error de usuario: Existen errores en tu formulario")
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