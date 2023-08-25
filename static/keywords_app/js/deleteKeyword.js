const deleteKeywordModal = document.getElementById("delete-keyword-modal")
const deleteKeywordBtn = document.getElementById("delete-keyword-btn")
const idEliminar = document.getElementById("id-eliminar")
const keyword = document.getElementById("keyword-eliminar")

deleteKeywordModal.addEventListener("show.bs.modal", () => {
    setTimeout(() => {
        var row = table.getRow(idActualizado)
        idEliminar.innerHTML = idActualizado
        keyword.innerHTML = row.getData().first_keyword + " | " + row.getData().second_keyword
    }, 1)
})