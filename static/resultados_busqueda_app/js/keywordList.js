var keyword
var keywordLinks = document.querySelectorAll(".keyword-link")

if (keywordLinks.length > 0) {
    setKeyword(keywordLinks[0].id)
    keywordLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault()
            setKeyword(link.getAttribute("id"))
            table.setData("/search-results/data/", { keyword: getKeyword() })
            event.stopPropagation()
        })
    })
} else {
    table.setData("/search-results/data/", { keyword: 0 })
}


function getKeyword() {
    return keyword
}

function setKeyword(valor) {
    keyword = valor
}

