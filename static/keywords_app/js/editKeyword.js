const editKeywordModal = document.getElementById("edit-keyword-modal")
editKeywordModal.addEventListener('show.bs.modal', event => {
    setTimeout(() => getKeywordById(idActualizado), 1)
})

async function getKeywordById(keyword_id) {
    try {
        const response = await fetch("/keywords/get/" + keyword_id, { method: "GET" })
        const json_response = await response.json()

        if (response.ok) {
            var editKeywordForm = document.getElementById("edit-keyword-form")
            fillFormWithData(json_response, editKeywordForm)
            manipulateKeywordsUIEditModal()
        } else if (response.status === 403) {
            showNotifications(response.status, json_response.error)
        } else {
            showNotifications(response.status, "Error interno en el servidor")
        }
    } catch (error) {
        console.log(error);
    }
}

const editKeywordForm = document.getElementById("edit-keyword-form").addEventListener("submit", event => {
    event.preventDefault();
    var formData = new FormData(event.target);
    editKeyword(formData, idActualizado)
})

async function editKeyword(formData, keyword_id) {
    try {
        const response = await fetch("/keywords/edit/" + keyword_id, { method: "POST", body: formData })
        const json_response = await response.json()
        if (response.ok) {
            window.location.href = `/search-results?keyword=${json_response.id}`
        } else if (response.status === 400) {
            setErrorsInForm(json_response, "error_edit_")
            showNotifications(response.status, "Error de usuario: Existen errores en tu formulario")
        } else if (response.status === 403) {
            showNotifications(response.status, json_response.error)
        } else {
            showNotifications(response.status, "Error interno en el servidor")
        }
    } catch (error) {
        console.log(error);
    }
}

editKeywordModal.addEventListener("hidden.bs.modal", () => {
    document.getElementById("edit-keyword-form").reset()
    var hiddenIdsOfSearchTerms = document.getElementsByClassName("search_terms_ids")
    for (let i = 0; i < hiddenIdsOfSearchTerms.length; i++) {
        const hiddenInput = hiddenIdsOfSearchTerms[i];
        hiddenInput.value = null
    }
    removeContainerIfExists()
    removeKeywordBoxes()
})
