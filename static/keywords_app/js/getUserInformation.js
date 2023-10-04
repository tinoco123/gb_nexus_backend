var userInformationModal = document.getElementById("user-information-modal")
userInformationModal.addEventListener('show.bs.modal', event => {
    setTimeout(() => getUserInformation(idActualizado), 1)
})

function getUserInformation(keyword_id) {
    var nombreSpan = document.getElementById("nombre")
    var apellidosSpan = document.getElementById("apellidos")
    var emailSpan = document.getElementById("email")
    var companySpan = document.getElementById("company")
    var lastLoginSpan = document.getElementById("last-login")
    fetch("/keywords/get/user-information/" + keyword_id, {
        method: "GET"
    })
        .then(response => {
            response.json()
                .then(data => {
                    if (response.ok) {
                        nombreSpan.innerHTML = data.first_name
                        apellidosSpan.innerHTML = data.last_name
                        emailSpan.innerHTML = data.email
                        companySpan.innerHTML = data.company
                        lastLoginSpan.innerHTML = data.last_login
                    }
                    else if (response.status >= 400 && response.status < 500) {
                        showNotifications(response.status, data.error)
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
