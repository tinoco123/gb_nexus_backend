var searchTermsModal = document.getElementById("search-terms-modal")
searchTermsModal.addEventListener('show.bs.modal', event => {
    setTimeout(() => getSearchTerms(idActualizado), 1)
})

function getSearchTerms(keyword_id) {
    fetch("/keywords/get/searchterms/" + keyword_id, {
        method: "GET"
    })
        .then(response => {
            response.json()
                .then(data => {
                    if (response.ok) {
                        var container = document.getElementById("modal-body")
                        var keywordTitle  = document.getElementById("keyword-title")
                        keywordTitle.innerHTML = "Keyword: " + data.keyword
                        container.innerHTML = ""
                        setSearchtTerms(data.data, container)
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

function setSearchtTerms(data, container) {
    for (let i = 0; i < data.length; i++) {
        var name = data[i].name
        var is_required = data[i].is_required == true ? "Verdadero" : "Falso"
        container.innerHTML += `
          <p>
            <strong>Término de búsqueda ${i+1}: </strong>
            ${name}  |
            <strong> Es obligatorio: </strong>
            ${is_required}
          </p>
        `
    }
}