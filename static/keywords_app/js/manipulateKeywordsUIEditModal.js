function manipulateKeywordsUIEditModal() {
    var editBoxes = document.getElementsByClassName("edit-box")

    editBoxes = Array.from(editBoxes)
    var boxesWithData = []
    var emptyBoxes = editBoxes.filter(editBox => {
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