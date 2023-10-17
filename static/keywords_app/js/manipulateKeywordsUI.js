document.addEventListener("DOMContentLoaded", () => {
    const createBoxes = document.getElementsByClassName("create-box")
    var notShowing = Array.from(createBoxes)
    var showing = []
    const addKeywordModalCreate = document.getElementById("add-keyword-modal-create")
    const deleteKeywordModalCreate = document.getElementById("delete-keyword-modal-create")

    addKeywordModalCreate.addEventListener("click", () => {
        if (notShowing.length >= 1) {
            var boxInputDeleted = notShowing.shift()
            boxInputDeleted.removeAttribute("hidden")
            showing.push(boxInputDeleted)
        }

    })
    deleteKeywordModalCreate.addEventListener("click", () => {
        if (showing.length >= 1) {
            var boxInputDeleted = showing.pop()
            boxInputDeleted.setAttribute("hidden", "")
            notShowing.push(boxInputDeleted)
        }
    })

})

