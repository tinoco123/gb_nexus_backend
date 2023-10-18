var boxesWithData = []
var emptyBoxes = []

const addKeywordModalEdit = document.getElementById("add-keyword-modal-edit")
const deleteKeywordModalEdit = document.getElementById("delete-keyword-modal-edit")

addKeywordModalEdit.addEventListener("click", () => {
    if (emptyBoxes.length >= 1) {
        var boxInputDeleted = emptyBoxes.shift()
        boxInputDeleted.removeAttribute("hidden")
        boxesWithData.push(boxInputDeleted)
    }
})

deleteKeywordModalEdit.addEventListener("click", () => {
    if (boxesWithData.length >= 1) {
        var boxInputDeleted = boxesWithData.pop()
        boxInputDeleted.setAttribute("hidden", "")
        emptyBoxes.unshift(boxInputDeleted)
        var input = boxInputDeleted.querySelector("input")
        input.value = ""
    }
})

function manipulateKeywordsUIEditModal() {
    var editBoxes = document.getElementsByClassName("edit-box")
    editBoxes = Array.from(editBoxes)
    boxesWithData = []
    emptyBoxes = editBoxes.filter(editBox => {
        var editBoxInputValue = editBox.querySelector("input").value
        if (editBoxInputValue.length != 0) {
            boxesWithData.push(editBox)
        }
        return editBoxInputValue.length === 0
    })
    showBoxesWithData(boxesWithData)
}

function showBoxesWithData(boxesWithData) {
    if (boxesWithData.length > 0) {
        boxesWithData.forEach(boxWithData => {
            boxWithData.removeAttribute("hidden")
        })
    }
}

function removeKeywordBoxes() {
    var editBoxes = Array.from(document.getElementsByClassName("edit-box"))
    editBoxes.forEach(editBox => {
        editBox.setAttribute("hidden", "")
    })
}
