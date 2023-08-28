var actionIcons = function () { //plain text value
    var accionHTML = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#modalVerResultadosBusqueda'><i class='bi bi-eye fs-5'></i></button> <button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#modalEliminarResultadoBusqueda'><i class='bi bi-trash fs-5'></i></button>"
    return accionHTML;
};

var table = new Tabulator("#searchResultsTable", {
    layout: "fitDataFill",
    placeholder: "Sin datos que mostrar",
    pagination: true,
    paginationMode: "remote",
    ajaxURL: "/search-results/data/",
    ajaxURLGenerator: function (url, config, params) {
        return url + "?page=" + params.page + "&size=" + params.size + "&keyword=" + getKeyword()
    },
    paginationSize: 10,
    paginationSizeSelector: [5, 10, 20, 30, 40, 50],
    paginationCounter: "rows",
    height: 680,
    columns: [
        {
            formatter: "rowSelection", titleFormatter: "rowSelection", hozAlign: "center", headerHozAlign: "center", resizable: false, headerSort: false, cellClick: function (e, cell) {
                cell.getRow().toggleSelect();
            }
        },
        { title: "id", field: "_id", visible: false },
        { title: "Página", field: "title", width: 500 },
        { title: "Fecha", field: "date", sorter: "date" },
        { title: "Estado", field: "state" },
        { title: "URL", field: "urlPage", width: 500 },
        { title: "Zona", field: "federalEstatal" },
        { title: "Acciones", formatter: actionIcons, width: 107, hozAlign: "center", headerHozAlign: "center", headerSort: false, frozen: true },
    ],
});

var rowSelected = null

table.on("rowClick", function (e, row) {
    rowSelected = row
})