var printIcon = function () { //plain text value
    var accionHTML = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#modalVerResultadosBusqueda'><i class='bi bi-eye fs-5'></i></button> <button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#modalEliminarResultadoBusqueda'><i class='bi bi-trash fs-5'></i></button>"
    return accionHTML;
};

var table = new Tabulator("#searchResultsTable", {
    layout: "fitDataFill",
    data: [], //set initial table data
    placeholder:"Sin datos que mostrar",
    pagination:true, //enable pagination
    paginationMode:"remote", //enable remote pagination
    ajaxURL:"",
    height: 550,
    columns: [
        {
            formatter: "rowSelection", titleFormatter: "rowSelection", hozAlign: "center", headerHozAlign: "center", resizable: false, headerSort: false, cellClick: function (e, cell) {
                cell.getRow().toggleSelect();
            }
        },
        { title: "Página", field: "pagina" },
        { title: "Fecha de publicación", field: "date", sorter: "date" },
        { title: "Estado", field: "estado" },
        { title: "URL", field: "url" },
        { title: "Zona", field: "zona" },
        { title: "Acciones", formatter: printIcon, width: 107, hozAlign: "center", headerHozAlign: "center", headerSort: false },
    ],
});
