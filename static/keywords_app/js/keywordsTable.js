var actionIcons = function (cell, formatterParams) {
    var actionHTML = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#edit-client-modal'><i class='bi bi-pen fs-5'></i></button> <button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#delete-client-modal'><i class='bi bi-trash fs-5'></i></button>"
    return actionHTML;
};

var table = new Tabulator("#keywordsTable", {
    layout: "fitDataFill",
    pagination: true,
    paginationMode: "remote",
    ajaxURL: "/keywords/data/",
    paginationSize: 10,
    paginationSizeSelector: [10, 20, 30, 40, 50],
    paginationCounter: "rows",
    height: 680,
    placeholder: "Sin datos que mostrar",
    columns: [
        {
            formatter: "rowSelection", titleFormatter: "rowSelection", hozAlign: "center", headerHozAlign: "center", resizable: false, headerSort: false, cellClick: function (e, cell) {
                cell.getRow().toggleSelect();
            }
        },
        { title: "ID", field: "id", sorter: "number" },
        { title: "Keyword 1", field: "first_keyword" },
        { title: "Keyword 2", field: "second_keyword" },
        { title: "Fecha de creación", field: "date_created" },
        { title: "Acciones", formatter: actionIcons, hozAlign: "center", headerHozAlign: "center", headerSort: false, width: 102 },
    ],
});

var idActualizado = 0
var rowIndex = 0

table.on("rowClick", function (e, row) {
    idActualizado = row.getData().id
    rowIndex = row.getIndex()
});