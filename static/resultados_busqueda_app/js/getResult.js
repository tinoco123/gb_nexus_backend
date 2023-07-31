var idActualizado

table.on("rowClick", function (e, row) {
    idActualizado = row.getData()._id
})

modalVerResultadosBusqueda = document.getElementById("modalVerResultadosBusqueda")
modalVerResultadosBusqueda.addEventListener('shown.bs.modal', event => {

})