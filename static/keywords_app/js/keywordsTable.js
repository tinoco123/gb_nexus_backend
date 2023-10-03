var actionIcons = function (cell, formatterParams) {
    var actionHTML = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#edit-keyword-modal'><i class='bi bi-pen fs-5'></i></button> <button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#delete-keyword-modal'><i class='bi bi-trash fs-5'></i></button>"
    return actionHTML;
};

var viewSearchTerms = function (cell, formatterParams) {
    var searchTermButton = "<button class='btn px-1 py-0' data-bs-toggle='modal' data-bs-target='#search-terms-modal'><i class='bi bi-key fs-4'></i></button>"
    return searchTermButton;
};

var table = new Tabulator("#keywordsTable", {
    layout: "fitDataFill",
    pagination: true,
    paginationMode: "remote",
    ajaxURL: "/keywords/data/",
    ajaxURLGenerator: function (url, config, params) {
        return url + "?page=" + params.page + "&size=" + params.size + "&keyword_type=" + getRadioSelected()
    },
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
        { title: "Título", field: "title" },
        { title: "Fecha de creación", field: "date_created" },
        { title: "Términos de búsqueda:", formatter: viewSearchTerms, hozAlign: "center", headerHozAlign: "center", headerSort: false },
        { title: "Acciones", formatter: actionIcons, hozAlign: "center", headerHozAlign: "center", headerSort: false, width: 102, frozen: true },
    ],
});

var idActualizado = 0
var rowIndex = 0

table.on("rowClick", function (e, row) {
    idActualizado = row.getData().id
    rowIndex = row.getIndex()
});