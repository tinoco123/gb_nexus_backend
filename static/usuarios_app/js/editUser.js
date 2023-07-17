var idActualizado = 0
table.on("rowClick", function(e, row){
    idActualizado = row.getData().id
});

const userModal = document.getElementById('userModal')
userModal.addEventListener('shown.bs.modal', event => {
})