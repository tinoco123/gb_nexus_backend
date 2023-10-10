var keyword

function assignLinksToEachKeyword() {
    var keywordLinks = document.querySelectorAll(".keyword-link")

    if (keywordLinks.length > 0) {
        setKeyword(keywordLinks[0].id)
        keywordLinks.forEach(function (link) {
            link.addEventListener("click", function (event) {
                event.preventDefault()
                setKeyword(link.getAttribute("id"))
                table.setData("/search-results/data/", { keyword: getKeyword() })
                    .then(() => {
                        showNotifications(200, "Resultados de keyword: " + link.textContent)
                    })
                event.stopPropagation()
            })
            link.addEventListener("contextmenu", async (event) => {
                event.preventDefault()
                try {
                    var response = await fetch("/keywords/get/user-information/" + link.id)
                    var data = await response.json()
                    if (response.status === 200) {
                        showUserInformation(data, event)
                    } else if (response.status === 405) {
                        showNotifications(response.status, data.error)
                    } else if (response.status === 403) {
                        showNotifications(response.status, data.error)
                    }
                } catch (error) {
                    console.log(error);
                    showNotifications(500, "Error en el servidor, intentelo más tarde")
                }
            })
        })
    } else {
        table.setData("/search-results/data/", { keyword: 0 })
    }

}


function getKeyword() {
    return keyword
}

function setKeyword(valor) {
    keyword = valor
}

