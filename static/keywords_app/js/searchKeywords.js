const searchInput = document.getElementById("search-keyword")
var search = ""
searchInput.addEventListener("keyup", (event) => {
    event.preventDefault()
    search = searchInput.value
                event.stopPropagation()
    table.setData("/keywords/data", {keyword_type: getRadioSelected(), search:search})
    event.stopPropagation()

})

function getSearchText() {
    return search
}